#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError, \
                     RawDescriptionHelpFormatter
import sys
import os
import re
import numpy as np
import pickle
import matplotlib.pyplot as plt

import gaussian_suite.gen_input as gsgi
import xyz_py as xyzp
import xyz_py.atomic as atomic
from molcas_suite.extractor import make_extractor as make_molcas_extractor
from gaussian_suite.extractor import make_extractor as make_gaussian_extractor
import gaussian_suite.cd_extractor as gscd
from hpc_suite.action import ParseKwargs, BooleanOptionalAction
from hpc_suite import parse_dict_key_only, parse_dict, SecondaryHelp
import angmom_suite
import angmom_suite.crystal as crystal
import molvis.core as mvis

from .distortion import Distortion, Dx, DistortionInfo
from .derivative import Finite, print_tau_style, read_tau_style
from .func import make_func
from .lvc import LVC, generate_lvc_input
from .vibrations import Harmonic
from . import cells

plt.rcParams['font.family'] = "Arial"


# Action for secondary function help message
class FunctionHelp(SecondaryHelp):
    def __call__(self, parser, namespace, values, option_string=None):

        if namespace.function == 'cfp':
            angmom_suite.read_args(['cfp', '--help'])
        else:
            raise ValueError("Supply valid option to function argument.")


def generate_distortion_func(args):

    labels, coords = xyzp.load_xyz(args.input)

    sp_data = DistortionInfo.from_file(args.distortion_info)

    coords += sp_data.make_distortion(args.distortion.axes).evaluate()

    if args.origin:
        origin = [lab.split('.')[0] for lab in labels].index(args.origin)
        coords -= coords[origin]

    xyzp.save_xyz(args.output, labels, coords)

    return


def init_func(args):
    sp_data = DistortionInfo.from_args(args)
    sp_data.to_file(args.distortion_info)

    return


def lvc_func(args):

    sp_data = DistortionInfo.from_file(args.distortion_info)

    V0th = {}
    W1st = {}

    sf_smult = make_molcas_extractor(args.rassi, ("rassi", "spin_mult"))[()]
    ener = make_molcas_extractor(args.rassi, ("rassi", "SFS_energies"))[()]

    for smult, nroots in zip(*np.unique(sf_smult, return_counts=True)):
        V0th[smult] = ener[smult == sf_smult]
        W1st[smult] = np.zeros((nroots, nroots, sp_data.natoms, 3))

    for grad_file in args.grad:

        grad = make_molcas_extractor(grad_file, ("gradients", None))

        for lab, val in iter(grad):
            smult, root = lab
            W1st[smult][root-1, root-1] = val

        nacs = make_molcas_extractor(grad_file, ("nacs", "CI"))

        for lab, val in iter(nacs):
            smult, root1, root2 = lab
            W1st[smult][root1-1, root2-1] = W1st[smult][root2-1, root1-1] = val

    sf_amfi = make_molcas_extractor(args.rassi, ("rassi", "SFS_AMFIint"))[()]
    sf_angm = make_molcas_extractor(args.rassi, ("rassi", "SFS_angmom"))[()]
    coords = make_molcas_extractor(
        args.rassi, ("rassi", "center_coordinates"))[()]

    lvc = LVC(V0th, W1st, sf_smult=sf_smult, sf_amfi=sf_amfi, sf_angm=sf_angm,
              coords=coords, verbose=True)

    lvc.to_file(args.lvc_data)

    return


def vib_func(args):

    if args.gaussian_log:
        ho = Harmonic.from_gaussian_log(args.gaussian_log)
        if args.mass:
            raise ValueError("The --mass argument is not available with freq "
                             "data read from Gaussian text output.")

    elif args.gaussian_fchk:
        ho = Harmonic.from_gaussian_fchk(
            args.gaussian_fchk, ext_masses=args.mass)

    elif args.force_sets:
        ho = Harmonic.from_vasp_phonopy(
            args.poscar,
            args.force_sets,
            supercell=args.distortion_expansion,
            force_expansion=args.force_expansion,
            ext_masses=args.mass
        )

    subset = None if args.active_atoms is None else \
        [idx - 1 for idc in args.active_atoms for idx in idc]

    ho.subset_atoms(subset).to_file(args.vibration_info)

    return


def summary_func(args):

    # read spin-phonon data
    sp_data = DistortionInfo.from_file(args.distortion_info)

    distortion_list = sp_data.generate_distortion_list()
    distortion_str = ' '.join([str(d) for d in distortion_list])

    distortion_count = len(distortion_list)

    if args.count:
        print(distortion_count)

    elif args.distortions:
        print(distortion_str)

    else:
        print("Number of distortion calculations: {}".format(distortion_count))
        print("Distortion list: {}".format(distortion_str))

    return


def prepare_func(args, unknown_args):

    if args.program == 'tau':
        # CFP args
        if args.lvc_data:
            cfp_args = angmom_suite.read_args(['cfp'] + unknown_args)
            cfp_args.theta = True
            cfp_args.space = cfp_args.space or cfp_args.ion.casscf_terms('s')
            cfp_args.symbol = cfp_args.symbol or {
                'l': cfp_args.ion.ground_term,
                'j': cfp_args.ion.ground_level
                }[cfp_args.basis]
            func_kwargs = vars(cfp_args)

        else:
            func_kwargs = {}

        # derivative args
        setattr(args, 'function', 'CFPs')
        setattr(args, 'zpd_unit', True)
        setattr(args, 'order', 1)
        setattr(args, 'max_analytic_order', None)
        setattr(args, 'format', 'tau')

        # EQ_CFPs.dat
        kq_idc = angmom_suite.crystal.stevens_kq_indices[:27]
        cfp_vals = make_func(args, **func_kwargs)(Distortion(), Dx())
        cfp_data = np.column_stack((np.ones(27), kq_idc, cfp_vals))
        np.savetxt('EQ_CFPs.dat', cfp_data,
                   fmt=['%2d', '%2d', '% 2d', '%16.8f'])

        # CFP_derivatives.dat
        derivatives_func(args, **func_kwargs)

        # mode_energies.dat
        ho = Harmonic.from_file(args.vibration_info)
        np.savetxt('mode_energies.dat', ho.freqs, fmt='%16.8f',
                   header="Frequency (cm-1)", comments='')

    return


def gen_charges_func(args):
    """
    Wrapper function for cli call to gen_charges
    """

    scell = cells.SuperCell.from_poscar(args.poscar, args.distortion_expansion)

    xyzp.save_xyz(
        "supercell.xyz", scell.atom_labels, scell.cart_coords, verbose=False
    )
    print()
    print("Supercell written to supercell.xyz")

    print("******************************")
    print("The unique entities are")
    for formula, indices in scell.asu_entities.items():
        print(formula)
    print("******************************")

    asu_indices = np.unique(scell.symmetry["equivalent_atoms"])

    xyzp.save_xyz(
        "unique_entities.xyz",
        scell.atom_labels[asu_indices],
        (scell.cart_coords + scell.repair_shifts)[asu_indices],
        verbose=False
    )
    print("Unique entities written to unique_entities.xyz\n")

    if len(asu_indices) < len(cells.flatten(scell.asu_entities.values())):
        print("\033[31m             ****Warning****") # noqa
        print("      High symmetry entity detected")
        print("Check calculated CHELPG charges obey symmetry \033[0m\n")

    # Create gaussian inputs for CHELPG calculation, one for each
    # member of the ASU

    # All electron aug-cc-pvtz
    ae_pvtz = [
        'H', 'Li', 'Be', 'Na', 'Mg', 'B', 'C', 'N', 'O', 'F', 'He', 'Ne', 'Al',
        'Si', 'P', 'S', 'Cl', 'Ar', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'
    ]
    ae_basis = {
        "{}".format(atoms): "aug-cc-pvtz"
        for atoms in ae_pvtz
    }

    unsupported = [
        "K", "Ca", "Rb", "Sr", "Cs", "Ba", "Ac", "Th", "Pa", "U", "Np",
        "Pu", "Am", "Cm"
    ]
    unsupported_basis = {
        "{}".format(atoms): "????"
        for atoms in unsupported
    }

    for lab in scell.atom_labels[cells.flatten(scell.asu_entities.values())]:
        if lab in unsupported:
            print("\033[31m Warning, add basis for {} to .com file\033[0m \n".format(lab)) # noqa
    ae_basis = ae_basis | unsupported_basis

    # ECP
    pp_pvtz = [
        'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'
    ]
    small_pp_basis = {
        "{}".format(atoms): "aug-cc-pvtz-pp"
        for atoms in pp_pvtz
    }

    stuttgart = {
        "{}".format(metals): "stuttgart rsc 1997"
        for metals in atomic.lanthanides + atomic.transition_metals
    }

    psuedo = small_pp_basis | stuttgart

    try:
        os.mkdir("gaussian")
    except OSError:
        pass

    for formula, indices in scell.asu_entities.items():
        gsgi.gen_input(
            "gaussian/{}.com".format(formula),
            scell.atom_labels[indices],
            (scell.cart_coords+scell.repair_shifts)[indices],
            99,
            99,
            method="PBE",
            bs_spec=ae_basis,
            ecp_spec=psuedo,
            opt=False,
            freq=False,
            extra_title="{}".format(formula),
            chelpg="charge"
        )
        print()

    print("\033[93mCharge and multiplicity set to 99 in all .com files")
    print("Please replace with actual values before submitting \033[0m \n")

    # Store supercell object in pickle for next step
    with open("supercell.pickle", 'wb') as _file:
        pickle.dump(scell, _file)

    print(
        "\033[0;32mSupercell object pickled in supercell.pickle \033[0m"
    )
    return


def parse_charges_func(args):
    """
    Wrapper function for cli call to parse_charges
    """

    # Load cell object from gen_charges
    with open(args.supercell_pickle, 'rb') as _file:
        scell: cells.Cell = pickle.load(_file)

    if args.calc_dir.lower() != 'cwd':
        calc_dir = "{}/".format(args.calc_dir)
    else:
        calc_dir = ""

    asu_charges = {
        head: gscd.get_chelpg_charges("{}/{}.log".format(calc_dir, head))
        for head in scell.asu_entities.keys()
    }

    index_to_charge = {
        index: charge
        for head in scell.asu_entities.keys()
        for index, charge in zip(scell.asu_entities[head], asu_charges[head])
    }

    supercell_charges = [
        index_to_charge[index] for index in scell.symmetry['equivalent_atoms']
    ]
    _min_charge = np.min(supercell_charges)
    _max_charge = np.max(supercell_charges)
    _charge_spread = _max_charge - _min_charge

    if args.vis_charges in ["entities", "all"]:

        viewers = []

        for it, indices in enumerate(scell.asu_entities.values()):
            # Get charge of current entity
            _charges = [supercell_charges[ind] for ind in indices]
            # Get labels and coords, and shift centre of mass to origin
            # so that interactive plot can be manipulated easily by user
            _labels = scell.atom_labels[indices]
            _coords = (scell.cart_coords+scell.repair_shifts)[indices]
            _coords -= xyzp.calculate_com(_labels, _coords)

            # Create Viewer object for current entity
            _tmp = cells.vis_charges_viewer(
                coords=_coords,
                labels=_labels,
                norm_charges=(_charges - _min_charge)/_charge_spread,
                viewer_style_args={
                    "height": "{}vh".format(95/len(asu_charges.keys())),
                    "width": "95vw"
                },
                viewer_div_args={
                    "div_id": "viewer_{:d}".format(it+1)
                }
            )
            viewers.append(_tmp)
        
        # Create webpage containing one viewer per entity with 
        # headers specifiying charge and colours
        body = [
            "<P> Maximum negative charge is {:f} e (Blue) </P>".format(
                _min_charge
            ),
            "<P> Maximum positive charge is {:f} e (Red) </P>".format(
                _max_charge
            ),
            "<P> Right click image to save </P>"
        ]
        body += [viewer.div for viewer in viewers]
        page = mvis.HtmlPage(
            scripts=[viewer.script for viewer in viewers],
            body=body
        )
        page.save("entities.html")
        print("\n\033[0;32mEntity charges can be visualised in entities.html\033[0m\n")

    central_atom = args.central_atom
    central_formula = args.central_formula

    # Pick user defined entity and move to centre of cell
    central_indices, without_central_indices = scell.find_centre_indices(
        central_formula=central_formula
    )

    catind = np.where(scell.atom_labels[central_indices] == central_atom)[0][0]
    catind = central_indices[catind]

    # Periodically recentre coordinates at central_formula
    scell.shift_centre_to(scell.frac_coords[catind])

    xyzp.save_xyz(
        "central_o_shifted.xyz",
        scell.atom_labels[central_indices],
        scell.cart_coords[central_indices]
    )

    xyzp.save_xyz(
        "environment_o_shifted.xyz",
        scell.atom_labels[without_central_indices],
        scell.cart_coords[without_central_indices]
    )

    # Make molcas basis file for environment charges
    _charges = [
        supercell_charges[wci] for wci in without_central_indices
    ]
    _coords = scell.cart_coords[without_central_indices]
    _labels = scell.atom_labels[without_central_indices]

    cells.make_molcas_basis_and_xyz(_labels, _coords, _charges)
    print("\033[93m")
    print("Molcas files for environment written to:")
    print("     ENV (basis set specification)")
    print("     molcas_environment.xyz (environment coordinates, use with molcas_suite generate_input --basis_xyz) \033[0m") # noqa

    np.savetxt(
        "environment_charges.dat",
        _charges
    )

    if args.vis_charges in ["supercell", "all"]:

        viewer = cells.vis_charges_viewer(
            coords=_coords,
            labels=_labels,
            norm_charges=(_charges - _min_charge)/_charge_spread,
            extra_coords=scell.cart_coords[central_indices],
            extra_labels=scell.atom_labels[central_indices],
            extra_color='#000000',
            viewer_style_args={
                "width":"95vw"
            },
            main_kwargs={"atom_opacities":0.5}
        )
        body = [
            "<P> Maximum negative charge is {:f} e (Blue) </P>".format(_min_charge),
            "<P> Maximum positive charge is {:f} e (Red) </P>".format(_max_charge),
            "<P> Right click image to save </P>",
            viewer.div
        ]
        page = mvis.HtmlPage(
            scripts=[viewer.script],
            body=body
        )

        page.save("supercell.html")
        print("\n\033[0;32mSupercell charges can be visualised in supercell.html\033[0m") #noqa

    return


def derivatives_func(args, unknown_args=None, **func_kwargs):

    if args.method == "findiff":
        dx = Finite.from_file(args.distortion_info)

    # parse extra function kwargs
    if not func_kwargs and unknown_args:
        if args.function == 'CFPs':
            func_kwargs = vars(angmom_suite.read_args(['cfp'] + unknown_args))
        elif not unknown_args:
            func_kwargs = {}
        else:
            raise ValueError("Unused extra arguments not known to the parser.")

    func = make_func(args, max_numerical_order=dx.order,
                     max_analytic_order=args.max_analytic_order, **func_kwargs)

    # prints derivatives and function values on the input grid
    if args.format == 'points':
        dx.write_points(
            args.function + "_points.dat", func, max_order=args.order)
        return

    ho = Harmonic.from_file(args.vibration_info)

    # remove normalisation and convert to units of zero point displacement
    conv = np.sqrt(ho.red_masses) * (ho.zpd if args.zpd_unit else 1.0)
    dQ = dx.transform(ho.displacements, func, args.order) * conv[:, np.newaxis]

    if args.format == 'tau':  # print central derivatives in tau style input

        if not args.order == 1:
            raise ValueError("Only first order derivatives with tau format.")

        if not args.function == 'CFPs':
            raise ValueError("Only function=CFPs possible with tau format.")

        print_tau_style(dQ, ho.freqs, 'CFP_polynomials.dat')

    else:  # print central derivatives to file
        pass

    return


def generate_lvc_input_func(args):

    # todo: make prettier by parsing numbers directly to list of ints using
    # parse_range and a custom action which flattens, check also other uses of
    # parse_range if flattened

    # todo: replace dict by global definition
    roots_dict = {'dy': [18]}

    if args.num_roots:
        num_roots = [int(n) for n in args.num_roots]
    elif args.ion:
        num_roots = roots_dict[args.ion.lower()]
    else:
        sys.exit("Invalid specification of the number of roots.")

    iph_idc = range(1, len(num_roots) + 1) \
        if args.jobiph is None else [int(i) for i in args.jobiph]

    for num_root, iph_idx in zip(num_roots, iph_idc):
        if args.dry:
            input_name = r"lvc_root{:0" + str(len(str(num_root))) + r"}"
            print(
                ' '.join(
                    [input_name.format(i) for i in range(1, num_root + 1)]
                )
            )
        else:
            generate_lvc_input(
                args.old_path,
                args.old_project,
                num_root,
                iph_idx,
                mclr_kwargs=args.mclr,
                alaska_kwargs=args.alaska
            )

    return


def parse_range(string):
    """
    adapted from https://stackoverflow.com/questions/6512280/accept-a-range-of-
    numbers-in-the-form-of-0-5-using-pythons-argparse
    """

    # match numbers in hyphen separated range
    # capture first and second string of digits, don't capture hyphon
    splt = re.match(r'(\d+)(?:-(\d+))?$', string)

    if not splt:
        raise ArgumentTypeError(
            "'{}' is not a range of number. Expected forms like '0-5' or '2'.".format( # noqa
                string
            )
        )

    # extract start and end of range, if single number is given -> end = start
    start = splt.group(1)
    end = splt.group(2) or start

    return list(range(int(start), int(end)+1))


def strength_func(args):
    """
    Wrapper for spin-phonon coupling strength CLI call
    """

    # Load CFP polynomials from file
    dQ, freqs = read_tau_style(args.cfp_file)

    # TODO delete
    args.n = 13
    args.J = 3.5
    args.L = 3
    args.S = 0.5

    if not args.nooef:
        # Get OEF values
        OEFs = crystal.calc_oef(args.n, args.J, args.L, args.S)
        print(np.shape(OEFs))

        # Add back in OEFs to polynomial values
        dQ *= OEFs

    # Calculate strength values of each mode
    S = np.array([crystal.calc_total_strength(mode) for mode in dQ])

    # Save strength to file
    np.savetxt("strengths.dat", S)
    print("Strengths saved to strengths.dat")

    # Read in symmetry labels if given
    if args.irreps:
        irreps = list(np.loadtxt(args.irreps, dtype=str))
    else:
        irreps = ['A']*len(freqs)

    unique_irreps, irrep_ints = np.unique(irreps, return_inverse=True)    

    if args.plot:

        _, ax = plt.subplots(num='Spin-phonon coupling strength')

        for unique_int in np.unique(irrep_ints):
            ax.stem(
                freqs[np.nonzero(irrep_ints == unique_int)[0]],
                S[np.nonzero(irrep_ints == unique_int)[0]],
                basefmt=' ',
                linefmt='C{:d}-'.format(unique_int),
                markerfmt='C{:d}o'.format(unique_int)
            )
        if args.irreps:
            ax.legend(unique_irreps, frameon=False)

        ax.set_ylabel(r'$S$ (cm$^{-1}$)', fontname="Arial")
        ax.set_xlabel('Mode energy (cm$^{-1}$)', fontname="Arial")

        ax.set_ylim([0., np.max(S)*1.05])

        plt.savefig("strengths.svg")
        plt.savefig("strengths.png")
        print("Strength plots saved to strengths.svg and strengths.png")
        plt.show()

    return


def read_args(arg_list=None):
    description = '''
    A package for performing Spin-Phonon coupling calculations.
    '''

    parser = ArgumentParser(
            description=description,
            formatter_class=RawDescriptionHelpFormatter
            )

    subparsers = parser.add_subparsers(dest='prog')

    distort = subparsers.add_parser('generate_distortion')
    distort.set_defaults(func=generate_distortion_func)

    distort.add_argument(
        'input',
        type=str,
        help='Input file containing the xyz-coordinates of the equilibrium structure.' # noqa
    )

    distort.add_argument(
        'output',
        type=str,
        help='Output file containing the xyz-coordinates of the distorted structure.' # noqa
    )

    distort.add_argument(
        '-D',
        '--distortion_info',
        type=str,
        help='HDF5 database file containing the normal mode displacement vectors.' # noqa
    )

    distort.add_argument(
        '--origin',
        type=str,
        help='Label of atom which stays fixed at the origin during distortion.'
    )

    distort.add_argument(
        '-d',
        '--distortion',
        required=True,
        type=Distortion.parse,
        help='Tuple consisting of <direction> (pos|neg) / <step_num> / <mode_index> ...' # noqa
    )

    init = subparsers.add_parser('init')
    init.set_defaults(func=init_func)

    init.add_argument(
        '-D',
        '--distortion_info',
        type=str,
        help='HDF5 database containing information about the distortion.'
    )

    init.add_argument(
        '--num_atoms',
        type=int,
        default=1,
        help='Number of atoms.'
    )

    init.add_argument(
        '--freq_gaussian',
        type=str,
        help='Gaussian output containing the normal mode information.'
    )

    init.add_argument(
        '--mode_wise',
        nargs='*',
        default=None,
        type=parse_range,
        help='Mode indices to be included in distortions calculations ' +
             '- activates mode-wise distortions.'
        )

    init.add_argument(
        '--atomic',
        nargs='*',
        default=None,
        type=parse_range,
        help='Atomic indices to be included in distortion calculations ' +
             '- activates atomic distortions.'
        )

    init.add_argument(
        '--num_steps',
        type=int,
        default=0,
        help='Number of distortion steps.'
    )

    init.add_argument(
        '--order',
        type=int,
        default=1,
        help='Order of distortion.'
    )

    init.add_argument(
        '--constant_step',
        type=float,
        help='Step size factor for constant displacement.'
    )

    info = subparsers.add_parser('summary')
    info.set_defaults(func=summary_func)

    info.add_argument(
        '-D',
        '--distortion_info',
        help='HDF5 database containing the spin-phonon information.'
    )

    select = info.add_mutually_exclusive_group(required=True)

    select.add_argument(
        '--distortions',
        default=False,
        action='store_true',
        help='Print list of distortions.'
    )

    select.add_argument(
        '--count',
        default=False,
        action='store_true',
        help='Print number of distortions.'
    )

    derive = subparsers.add_parser('derivatives')
    derive.set_defaults(func=derivatives_func)

    derive.add_argument(
        '-H',
        '--Help',
        action=FunctionHelp,
        help='show help message for additional arguments and exit'
    )

    derive.add_argument(
        'function',
        type=str,
        help='Function to derive.'
    )

    derive.add_argument(
        '--method',
        type=str,
        default="findiff",
        choices=["findiff", "polynomial"],
        help='Differentiation method'
    )

    evaluation = derive.add_mutually_exclusive_group(required=True)

    evaluation.add_argument(
        '-G',
        '--grid_data',
        type=str,
        help='HDF5 database containing the function values at distorted geometries.' # noqa
    )

    evaluation.add_argument(
        '-L',
        '--lvc_data',
        type=str,
        help='HDF5 database containing the LVC parameters.'
    )

    derive.add_argument(
        '-V',
        '--vibration_info',
        type=str,
        help='HDF5 database containing information about the vibrations.'
    )

    derive.add_argument(
        '-D',
        '--distortion_info',
        type=str,
        help='HDF5 database containing the distortion information.'
    )

    derive.add_argument(
        '--order',
        type=int,
        default=1,
        help='Order of derivative.'
    )

    derive.add_argument(
        '--max_analytic_order',
        type=int,
        help=(
            'Maximum analytic derivative order available for function.'
            'Defaults to 0 for grid data and 1 for LVC function data.'
        )
    )

    derive.add_argument(
        '--format',
        choices=['tau', 'points'],
        help='Output in <CFP_polynomials.dat> style.'
    )

    derive.add_argument(
        '--zpd_unit',
        default=False,
        action='store_true',
        help='Convert to units of zero point displacement.'
    )

    inp = subparsers.add_parser('generate_input')
    inp.set_defaults(func=generate_lvc_input_func)

    inp.add_argument(
        'old_project',
        type=str,
        help='Project name of preceding Molcas calculation.'
    )

    inp.add_argument(
        '--old_path',
        type=str,
        default='../',
        help='Path to WorkDir of preceding Molcas calculation.'
    )

    roots = inp.add_mutually_exclusive_group(required=True)

    roots.add_argument(
        '--num_roots',
        nargs='+',
        help='Number of states per JOBIPH.'
    )

    roots.add_argument(
        '--ion',
        type=str,
        help='Label of the metal center, e.g. Dy.'
    )

    inp.add_argument(
        '--jobiph',
        nargs='+',
        help='Indices of Molcas JOBIPH wavefunction files *_IPH.'
    )

    inp.add_argument(
        '--mclr',
        nargs='+',
        default=None,
        type=parse_dict_key_only,
        action=ParseKwargs,
        help='Manually run mclr with custom options, e.g. thre=1e-8',
        metavar='name=value')

    inp.add_argument(
        '--alaska',
        nargs='+',
        default=None,
        type=parse_dict_key_only,
        action=ParseKwargs,
        help='Run alaska with custom options, e.g. cuto=1e-8',
        metavar='name=value')

    inp.add_argument(
        '--dry',
        default=False,
        action='store_true',
        help='Dry-run which prints files to be created'
    )

    lvc = subparsers.add_parser('lvc')
    lvc.set_defaults(func=lvc_func)

    lvc.add_argument(
        '-D', '--distortion_info',
        type=str,
        help='HDF5 database containing information about the distortion.'
    )

    lvc.add_argument(
        '-L', '--lvc_data',
        type=str,
        help='HDF5 database output containing the LVC data.'
    )

    lvc.add_argument(
        '--grad',
        type=str,
        nargs='+',
        help='Molcas output file(s) containing gradients and NACs.'
    )

    lvc.add_argument(
        '--rassi',
        type=str,
        help=('Molcas *.rassi.h5 output file containing AMFI integrals, '
              'SF_ANGMOM operators and the spin multiplicities.')
    )

    vibrate = subparsers.add_parser('vib')
    vibrate.set_defaults(func=vib_func)

    vibrate.add_argument(
        '-V', '--vibration_info',
        type=str,
        help='HDF5 database containing information about the vibrations.'
    )

    vib_calc_excl = vibrate.add_mutually_exclusive_group(required=True)

    vib_calc_excl.add_argument(
        '--gaussian_log',
        type=str,
        help='Text output of a gaussian freq calculation.'
    )

    vib_calc_excl.add_argument(
        '--gaussian_fchk',
        type=str,
        help='Formatted checkpoint file of a gaussian freq calculation.'
    )

    vib_calc_excl.add_argument(
        '--force_sets',
        type=str,
        help='FORCE_SETS file from VASP-phonopy pre-process.'
    )

    vibrate.add_argument(
        '--poscar',
        type=str,
        help='Unit cell POSCAR from VASP-phonopy pre-process.'
    )

    vibrate.add_argument(
        '--distortion_expansion',
        nargs=3,
        metavar=('N_x', 'N_y', 'N_z'),
        type=int,
        help='Supercell expansion.'
    )

    vibrate.add_argument(
        '--force_expansion',
        nargs=3,
        metavar=('N_x', 'N_y', 'N_z'),
        default=(1, 1, 1),
        type=int,
        help='Supercell expansion used in phonon calculation'
    )

    vibrate.add_argument(
        '--mass',
        type=parse_dict,
        default={},
        nargs='+',
        action=ParseKwargs,
        help='Modify atomic masses for isotopic substitiution.',
        metavar='atom_index=mass'
    )

    vibrate.add_argument(
        '--trans',
        action=BooleanOptionalAction,
        default=True,
        help='Project out three rigid body translations.'
    )

    vibrate.add_argument(
        '--rot',
        action=BooleanOptionalAction,
        default=True,
        help='Project out three rigid body rotations.'
    )

    vibrate.add_argument(
        '--active_atoms',
        nargs='*',
        type=parse_range,
        help=(
            'Atomic indices active during spin-phonon coupling. Effectively'
            ' subsets the displacement vectors. Useful if coupling is '
            'evaluated with a subset of the atoms present in the vibrational'
            ' calculation.'
        )
    )

    prepare = subparsers.add_parser('prep')
    prepare.set_defaults(func=prepare_func)

    prepare.add_argument(
        'program',
        choices=['tau'],
        help='Program for which to prepare inputs.'
    )

    data = prepare.add_argument_group('database files')

    data.add_argument(
        '-G', '--grid_data',
        help=('HDF5 database containing the function values at distorted '
              'geometries.')
    )

    data.add_argument(
        '-L', '--lvc_data',
        help='HDF5 database containing the LVC parameters.')

    data.add_argument(
        '-V', '--vibration_info',
        help='HDF5 database containing information about the vibrations.')

    data.add_argument(
        '-D', '--distortion_info',
        help='HDF5 database containing the distortion information.')

    prepare.add_argument(
        '--method',
        type=str,
        default="findiff",
        choices=["findiff", "polynomial"],
        help='Differentiation method'
    )

    gen_charges = subparsers.add_parser(
        "gen_charges",
        description="""
        Creates inputs for Gaussian CHELPG charge calculations of each
        entity in the asymmetric unit of a VASP optimised structure
        """)
    gen_charges.set_defaults(func=gen_charges_func)

    gen_charges.add_argument(
        "poscar",
        type=str,
        help='Poscar containing optimised geometry'
    )

    gen_charges.add_argument(
        "distortion_expansion",
        type=int,
        nargs=3,
        help=(
            "Expansion used to generate supercell for spin phonon coupling"
            "calculations"
        )
    )

    parse_charges = subparsers.add_parser(
        "parse_charges",
        description=(
            "Collects result of Gaussian CHELPG charge calculations and maps"
            "charges back onto supercell coordinates."
        )
    )
    parse_charges.set_defaults(func=parse_charges_func)

    parse_charges.add_argument(
        "central_formula",
        type=str,
        help=(
            "Formula of central SMM or entity"
            "must match one of those given by gen_charges"
        )
    )

    parse_charges.add_argument(
        "central_atom",
        type=str,
        help='Central of central_formula, e.g. Dy'
    )

    parse_charges.add_argument(
        "--supercell_pickle",
        type=str,
        default='supercell.pickle',
        help='Supercell object pickle file'
    )

    parse_charges.add_argument(
        "--calc_dir",
        type=str,
        default='gaussian',
        help=(
            'Directory containing Gaussian .log file(s) with CHELPG charges'
            ' set to CWD for current directory'
        )
    )

    parse_charges.add_argument(
        "--vis_charges",
        type=str,
        help=(
            'Creates html file to visualise charges for entities and supercell'
        ),
        choices=("none", "all","supercell","entities")
    )

    strength = subparsers.add_parser('strength')
    strength.set_defaults(func=strength_func)

    strength.add_argument(
        "cfp_file",
        type=str,
        help=(
            "File (hdf5 or CFP_polynomials) containing coupling crystal",
            "field parameters"
        )
    )

    strength.add_argument(
        "n",
        type=float,
        help=(
            "Number of unpaired electrons in 4f subshell"
        )
    )

    strength.add_argument(
        "J",
        type=float,
        help=(
            "Total angular momentum quantum number"
        )
    )

    strength.add_argument(
        "L",
        type=float,
        help=(
            "Orbital angular momentum quantum number"
        )
    )

    strength.add_argument(
        "S",
        type=float,
        help=(
            "Spin angular momentum quantum number"
        )
    )

    strength.add_argument(
        "--plot",
        action="store_true",
        help="Produce plot of strength as a function of mode energy"
    )

    strength.add_argument(
        '--irreps',
        type=str,
        metavar='<file_name>',
        help=(
            'Color code strength plot based on mode symmetries listed in file',
            'file must contain column of IRREPs, one per mode'
        )
    )

    strength.add_argument(
        "--nooef",
        action="store_true",
        help="Produce plot of strength as a function of mode energy"
    )

    # If arg_list==None, i.e. normal cli usage, parse_args() reads from
    # "sys.argv". The arg_list can be used to call the argparser from the
    # back end.

    # read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    _args, _ = parser.parse_known_args(arg_list)

    # select parsing option based on sub-parser
    if _args.prog in ['derivatives', 'prep']:
        args, hpc_args = parser.parse_known_args(arg_list)
        args.func(args, hpc_args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)


def main():
    read_args()
