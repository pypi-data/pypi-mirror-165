from operator import add
from functools import reduce
import numpy as np
import h5py
import phonopy
from phonopy.harmonic.dynmat_to_fc import get_commensurate_points

from gaussian_suite.extractor import make_extractor as make_gaussian_extractor

from .cells import SuperCell

C0 = np.float(299792458)
BOHR2M = np.float(5.29177210903e-11)
AMU = np.float(1.66053906660e-27)
HARTREE2J = np.float(4.3597447222071e-18)
EV2J = np.float(1.602176634e-19)
H_PCK = np.float(6.62607015E-34)


class Harmonic:
    """Set of indenpendent quantum harmonic oscillators defined by their
    frequencies, displacements and reduced masses. The coordinate system
    follows the same conventions as the Gaussian software, i.e. the cartesian
    displacements are normalised and the normalisation constant is absorbed
    into the reduced mass.

    Parameters
    ----------
    freqs : np.array
        Array of harmonic frequencies in cm^-1.
    displacements : np.array
        K x N x 3 array containing the normalised displacement vectors.
    red_masses : np.array
        Array of the reduced masses.

    Attributes
    ----------
    freqs : np.array
        Array of harmonic frequencies in units of cm^-1.
    displacements : np.array
        K x N x 3 array containing the normalised displacement vectors.
    red_masses : np.array
        Array of the reduced masses in units of amu.
    natoms : int
        Number of atoms.
    nmodes : int
        Number of modes.
    force_const : np.array
        Array of force constants in units of mdyne/ang or N/cm.
    zpd : np.array
        Array of zero point displacements in ang.
    """

    def __init__(self, freqs, red_masses, displacements, weights=None):

        self.natoms = displacements.shape[1]
        self.nmodes = displacements.shape[0]

        if freqs.shape[0] != self.nmodes or red_masses.shape[0] != self.nmodes:
            raise ValueError("Dimensions of HO parameters do not match.")

        self.freqs = freqs
        self.displacements = displacements
        self.red_masses = red_masses
        # fill with scalar OR array provided by weight
        self.weights = \
            np.full((self.nmodes,), 1.0 if weights is None else weights)

    @property
    def force_const(self):
        # 10^8: N -> milliDyne, 10^-10: m^-1 -> ang^-1
        # final unit: mDyne/ang or N/cm
        return 1e8 * 1e-10 * \
            (2 * np.pi * self.freqs * 100)**2 * C0**2 * self.red_masses * AMU

    @property
    def zpd(self):
        # 10^10: m -> ang
        return 1e10 * np.sqrt(H_PCK * self.freqs * C0 / self.force_const)

    def to_file(self, h_file):

        with h5py.File(h_file, 'w') as h:
            h['/'].attrs.create('num_modes', self.natoms)
            h['/'].attrs.create('num_atoms', self.natoms)
            h.create_dataset('displacements', data=self.displacements)
            h.create_dataset('frequencies', data=self.freqs)
            h.create_dataset('reduced_masses', data=self.red_masses)
            h.create_dataset('weights', data=self.weights)

    def subset_atoms(self, active_atom_idc=None):
        if active_atom_idc is None:
            return self
        else:
            return self.__class__(self.freqs, self.red_masses,
                                  self.displacements[:, active_atom_idc])

    @classmethod
    def from_file(cls, h_file):

        with h5py.File(h_file, 'r') as h:
            displacements = h['displacements'][...]
            freqs = h['frequencies'][...]
            red_masses = h['reduced_masses'][...]

        return cls(freqs, red_masses, displacements)

    @classmethod
    def from_gaussian_log(cls, f):
        freqs = make_gaussian_extractor(f, ("freq", "frequency"))[1]
        modes = make_gaussian_extractor(f, ("freq", "displacement"))[1]
        red_masses = make_gaussian_extractor(f, ("freq", "reduced_mass"))[1]
        return cls(freqs, red_masses, modes)

    @classmethod
    def from_gaussian_fchk(cls, f, ext_masses=None, **kwargs):
        hess = make_gaussian_extractor(f, ('fchk', 'hessian'))[()]
        masses = make_gaussian_extractor(f, ('fchk', 'atomic_mass'))[()]

        for mdx, mass in ext_masses.items():
            masses[mdx - 1] = mass

        coords = make_gaussian_extractor(f, ('fchk', 'coordinates'))[()]
        return cls.analysis(hess, masses, coords=coords, **kwargs)

    @classmethod
    def from_vasp_phonopy(cls, poscar, force_sets, supercell=(1, 1, 1),
                          ext_masses=None, force_expansion=(1, 1, 1)):
        """Evaluate harmonic oscillators from VASP-phonopy calculation based
        on 
        """
        cell = phonopy.load(
            unitcell_filename=poscar,
            force_sets_filename=force_sets,
            supercell_matrix=force_expansion
        )

        _masses = cell._dynamical_matrix._pcell.masses
        masses = [ext_masses[mdx + 1] if ext_masses and mdx + 1 in ext_masses
                  else _masses[mdx] for mdx, m in enumerate(_masses)]

        if ext_masses:
            cell._dynamical_matrix._pcell.masses = masses
            cell._set_dynamical_matrix()

        q_points = get_commensurate_points(np.diag(supercell))

        cell.run_qpoints(q_points, with_eigenvectors=True)
        qpoint_dict = cell.get_qpoints_dict()

        vib_info = zip(
            q_points,
            qpoint_dict['frequencies'] * 1e12 / (C0 * 1e2),  # convert to cm^-1
            qpoint_dict['eigenvectors']
        )

        ho_list = []

        sfrac_coords = SuperCell.from_poscar(poscar, supercell).frac_coords \
            @ np.diag(supercell)
        n_cell = np.prod(supercell)

        for q_point, freqs, vecs in vib_info:
            print(f"Evaluating q-point {q_point}")

            phase = np.exp(-2.j * np.pi * sfrac_coords[0] @ q_point) * \
                np.repeat(np.exp(2.j * np.pi * sfrac_coords @ q_point), 3)
            svecs = phase[:, np.newaxis] / np.sqrt(n_cell) * \
                np.tile(vecs, (n_cell, 1))
            # print(np.allclose(svecs.imag, 0))
            # print(np.allclose(svecs.T.conj() @ svecs, np.identity(len(vecs))))
            red_masses, displacements = \
                normalised_mass_weighted(svecs.real, np.tile(masses, n_cell))
            ho_list.append(cls(freqs, red_masses, displacements))

        return reduce(add, ho_list)

    def __add__(self, other):

        _freqs = np.concatenate((self.freqs, other.freqs))
        order = np.argsort(_freqs)

        freqs = _freqs[order]
        displacements = \
            np.concatenate((self.displacements, other.displacements))[order]
        red_masses = np.concatenate((self.red_masses, other.red_masses))[order]
        weights = np.concatenate((self.weights, other.weights))[order]

        return self.__class__(freqs, red_masses, displacements, weights)

    @classmethod
    def analysis(cls, hessian, masses, trans=True, rot=True, coords=None):

        natom = len(masses)

        mwhess = hessian / np.sqrt(np.repeat(masses, 3)[np.newaxis, :] *
                                   np.repeat(masses, 3)[:, np.newaxis])

        eig, vec = np.linalg.eigh(mwhess)

        if trans:
            tra_frame = [np.array([d * np.sqrt(m) for m in masses for d in v])
                         for v in np.identity(3)]
            ntra = 3
        else:
            tra_frame = []
            ntra = 0

        if rot:
            # compute principle axis frame
            nrot, _, vec_inertia = principle_axis_inertia(masses, coords)

            # convert coordinates to principle axis frame
            # _coords = shift_to_com(masses, coords) @ vec_inertia.T
            _coords = shift_to_com(masses, coords)

            rot_frame = \
                [np.array([d * np.sqrt(m) for m, c in zip(masses, _coords)
                           for d in np.cross(c, v)])
                 for v in vec_inertia[:, (3 - nrot):].T]
        else:
            rot_frame = []
            nrot = 0

        nrotra = ntra + nrot
        nmodes = 3 * natom - nrotra

        rotra_frame = \
            np.array([d / np.linalg.norm(d) for d in tra_frame + rot_frame])

        if len(rotra_frame) != 0:
            # detect rigid body motions
            int_mask = np.logical_not(np.isclose(
                np.sum((rotra_frame @ vec)**2, axis=0), 1.0, rtol=1e-1))
            # Schmidt orthogonalisation
            new_frame, _ = np.linalg.qr(
                np.column_stack((rotra_frame.T, vec[:, int_mask])))
            # set coordinate frame to internal coordiantes
            frame = new_frame[:, nrotra:]

            # transfrom Hessian to internal coordinate frame and project out
            # rigid body motions
            eig, vec = np.linalg.eigh(frame.T @ mwhess @ frame)
            cart = frame @ vec / np.sqrt(np.repeat(masses, 3)[:, np.newaxis])

        else:
            cart = vec / np.sqrt(np.repeat(masses, 3)[:, np.newaxis])

        freqs = np.sqrt(eig * (HARTREE2J / BOHR2M**2 / AMU) /
                        (4*np.pi**2 * C0**2) + 0.j) / 100
        _freqs = np.vectorize(lambda x: -x.imag if x.imag else x.real)(freqs)

        red_masses = 1 / np.sum(cart**2, axis=0)
        displacements = \
            np.reshape((cart * np.sqrt(red_masses)).T, (nmodes, natom, 3))

        return cls(_freqs, red_masses, displacements)


def normalised_mass_weighted(vecs, masses):
    """Mass-weight eigenvectors and normalise. Normalisation constant is
    returned as reduced mass"""

    ndofs, nmodes = vecs.shape
    cart = vecs / np.sqrt(np.repeat(masses, 3)[:, np.newaxis])

    red_masses = 1 / np.sum(cart**2, axis=0)
    displacements = \
        np.reshape((cart * np.sqrt(red_masses)).T, (nmodes, ndofs // 3, 3))

    return red_masses, displacements


def shift_to_com(masses, coords):
    print(type(masses))
    com = np.sum(masses[:, np.newaxis] * coords, axis=0) / np.sum(masses)
    return coords - com


def principle_axis_inertia(masses, coords):

    _coords = shift_to_com(masses, coords)

    inertia = np.zeros((3, 3))
    inertia[0, 0] = np.sum(masses * (_coords[:, 1]**2 + _coords[:, 2]**2))
    inertia[1, 1] = np.sum(masses * (_coords[:, 2]**2 + _coords[:, 0]**2))
    inertia[2, 2] = np.sum(masses * (_coords[:, 0]**2 + _coords[:, 1]**2))
    inertia[1, 0] = -np.sum(masses * (_coords[:, 0] * _coords[:, 1]))
    inertia[2, 0] = -np.sum(masses * (_coords[:, 0] * _coords[:, 2]))
    inertia[2, 1] = -np.sum(masses * (_coords[:, 1] * _coords[:, 2]))
    inertia[0, 1] = inertia[1, 0]
    inertia[0, 2] = inertia[2, 0]
    inertia[1, 2] = inertia[2, 1]

    eig_inertia, vec_inertia = np.linalg.eig(inertia)
    rank = np.linalg.matrix_rank(inertia)

    if rank > 1:
        return rank, eig_inertia, vec_inertia
    else:
        raise ValueError("Rank of moment of inertia tensor smaller than one.")

