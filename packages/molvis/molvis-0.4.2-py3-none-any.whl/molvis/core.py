from re import L
import numpy as np
import xyz_py as xyzp

from . import utils as ut


class Viewer():
    """
    Wrapper for 3Dmol.js GLViewer class

    Parameters
    ----------
    objects : list[str], optional
        List of string objects/commands added to viewer callback function.
        e.g. output from `core.Model`
        ```
        ms1 = core.Model.from_xyz(xyz_file)
        viewer_1 = core.Viewer(objects=[ms1])
        ```

    extra_div_args : dict, optional
        Extra arguments passed to viewer div
    extra_style_args : dict, optional
        Extra arguments passed to style property of viewer div
    rc_download : bool, default True
        Enables right-click download of model on webpage
    
    Attributes
    ----------
    objects : list[str], optional
        List of molvis objects added to viewer callback function whose
        __repr__ will be called via str()
        e.g. `core.Model`
        ```
        ms1 = core.Model.from_xyz(xyz_file)
        viewer_1 = core.Viewer(objects=[ms1])
        ```
    div_id : str
        viewer div id string
    height : str
        viewer div height as string
    width : str
        viewer div width as string
    position : str
        viewer div position as string
    style : dict
        viewer div style, contains height, width and position. Can
        be overwritten completely.
    div_args : dict
        viewer div properties, including div_id, style, class, and
        background colour
    rc_download : bool
        Enables right-click download of model on webpage
    """

    def __init__(self, extra_div_args={}, extra_style_args={},
                 rc_download=True, objects=[]):
        
        self.div_args = {}
        self.style = {}

        self.div_id = "viewer"
        self.height = "100vh"
        self.width = "100vw"
        self.position = "relative"

        if len(extra_style_args):
            for esa_key, esa_val in extra_style_args.items():
                self.style[esa_key] = esa_val

        self.div_args = {
            "div_id": self.div_id,
            "style": self.style,
            "data-backgroundcolor": "0xf6f6f6"
        }

        if len(extra_div_args):
            for eda_key, eda_val in extra_div_args.items():
                self.div_args[eda_key] = eda_val

        self.div_args["data-callback"] = "make_model_{}".format(
            self.div_args["div_id"]
        )

        self.objects = [object for object in objects]

        self.rc_download = rc_download

        return

    @property
    def div_id(self):
        return self._div_id

    @div_id.setter
    def div_id(self, div_id: str):
        if not isinstance(div_id, str):
            raise TypeError("div_id should be str")
        self._div_id = div_id
        self.div_args["div_id"] = self._div_id
        return

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: str):
        if not isinstance(height, str):
            raise TypeError("height should be str")
        self._height = height
        self._style["height"] = self._height
        return
    
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: str):
        if not isinstance(width, str):
            raise TypeError("width should be str")
        self._width = width
        self._style["width"] = self._width
        return

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: str):
        if not isinstance(position, str):
            raise TypeError("position should be str")
        self._position = position
        self._style["position"] = self._position
        return

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style: dict):
        if not isinstance(style, dict):
            raise TypeError("style should be dict")
        self._style = style

        # Set private height, width, position if present
        if "height" in self._style.keys():
            self._height = self._style["height"]
        if "width" in self._style.keys():
            self._width = self._style["width"]
        if "position" in self._style.keys():
            self._position = self._style["position"]
        return

    @property
    def div_args(self):
        return self._div_args

    @div_args.setter
    def div_args(self, div_args: dict):
        if not isinstance(div_args, dict):
            raise TypeError("div_args should be dict")
        self._div_args = div_args
        # Class cannot change
        self._div_args["class"] = "viewer_3Dmoljs"

        # Set private div_id, background colour, style if present
        if "style" in self._div_args.keys():
            self.style = self._div_args["style"]
        if "div_id" in self._div_args.keys():
            self._div_id = self._div_args["div_id"]
        return


    @property
    def rc_download(self):
        return self._rc_download

    @rc_download.setter
    def rc_download(self, rc_download: bool):
        if not isinstance(rc_download, bool):
            raise TypeError("rc_download should be bool")
        self._rc_download = rc_download
        return


    def add_object(self, object):
        self.objects.append(object)
        return

    @property
    def div(self) -> str:

        string = "<div "

        for key, value in self.div_args.items():
            string += "{}='{}' ".format(key, self.unpack_dict(value))

        string += "></div>\n\n"

        return string

    @property
    def script(self) -> str:

        string = "    var {} = function(viewer)".format(self.div_args["data-callback"])
        string += "{\n"
        for object in self.objects:
            string += str(object)
        string += "        viewer.render();\n"
        string += "        viewer.zoomTo();\n"
        string += "        viewer.render();\n"

        if self.rc_download:
            string += "        $('canvas').bind('contextmenu', function(e) {\n"
            string += "            var duri = viewer.getCanvas().toDataURL('image/png', 1)\n" # noqa
            string += "            downloadURI(duri, 'molecule.png');\n"
            string += "            });\n"
            string += "    }\n\n"

            string += "    function downloadURI(uri, name) {\n"
            string += "        var link = document.createElement('a');\n"
            string += "        link.download = name;\n"
            string += "        link.href = uri;\n"
            string += "        document.body.appendChild(link);\n"
            string += "        link.click();\n"
            string += "        document.body.removeChild(link);\n"
            string += "    }\n"

        return string

    @classmethod
    def unpack_dict(cls, maybe_dict: dict or str):

        if isinstance(maybe_dict, str):
            string = "{}".format(maybe_dict)
        elif isinstance(maybe_dict, dict):
            string = ""
            for key, value in maybe_dict.items():
                string += "{}:{}; ".format(
                    key,
                    cls.unpack_dict(value)
                )
            string += ""
        else:
            exit()

        return string



class Model():
    """
    Wrapper for 3Dmol.js GLModel class

    Parameters
    ----------
    labels : list
        atomic labels
    coords : list
        atomic coordinates in angstrom

    Attributes
    ----------
    objects : list[str], optional
        List of molvis objects added to viewer callback function whose
        __repr__ will be called via str()
        e.g. `core.Model`
        ```
        ms1 = core.Model.from_xyz(xyz_file)
        viewer_1 = core.Viewer(objects=[ms1])
        ```
    div_id : str
        viewer div id string
    height : str
        viewer div height as string
    width : str
        viewer div width as string
    position : str
        viewer div position as string
    style : dict
        viewer div style, contains height, width and position. Can
        be overwritten completely.
    div_args : dict
        viewer div properties, including div_id, style, class, and
        background colour
    rc_download : bool
        Enables right-click download of model on webpage
    """
    def __init__(self, labels, coords, **kwargs) -> None:

        self.coords = coords
        self.labels = labels
        self.labels_nn = xyzp.remove_label_indices(labels)
        self.n_atoms = len(self.labels_nn)

        self.neighbourlist = xyzp.get_neighborlist(
            labels, coords, adjust_cutoff={"Y": 1.4}
        )
        self.bonds = xyzp.get_bonds(
            labels, coords, neigh_list=self.neighbourlist, verbose=False
        )
        self.adjacency = xyzp.get_adjacency(
            labels, coords, adjust_cutoff={"Y": 1.4}
        )

        self.model_js_var = "m"
        # Atom representation type, "stick", "sphere", "cartoon"
        self.atom_rep = "stick"

        # Dictionary, one per atom specifying a single style for that atom
        self.atom_styles = [
            {}
            for _ in range(self.n_atoms)
        ]

        # Supported atom style properties
        self.atom_colours = [
            ut.ATOM_COLOURS[label] if label in ut.ATOM_COLOURS.keys()
            else ut.ATOM_COLOURS["other"]
            for label in self.labels_nn
        ]
        self.atom_opacities = 1.
        self.atom_radii = .3

        self.extra_styles = []

        # Set kwargs
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        
        return

    @classmethod
    def from_xyz(cls, xyz_file, **kwargs):
        labels, coords = xyzp.load_xyz(xyz_file)

        return cls(labels, coords, **kwargs)

    @property
    def atom_rep(self):
        return self._atom_rep

    @atom_rep.setter
    def atom_rep(self, atom_rep: list):

        if not isinstance(atom_rep, (list, str)):
            raise TypeError("atom_rep should be either list or str")
        elif isinstance(atom_rep, str):
            self._atom_rep = [
                atom_rep for it in range(self.n_atoms)
            ]
        elif isinstance(atom_rep, list) and len(atom_rep) == self.n_atoms:
            self._atom_rep = atom_rep
        else:
            raise ValueError("Number of rep should be 1 or n_atoms")

        return

    @property
    def atom_opacities(self):
        return self._atom_opacities

    @atom_opacities.setter
    def atom_opacities(self, atom_opacities: list):

        if not isinstance(atom_opacities, (list, float)):
            raise TypeError("atom_opacities should be either list or float")
        elif isinstance(atom_opacities, float):
            self._atom_opacities = [
                atom_opacities for _ in range(self.n_atoms)
            ]
        elif len(atom_opacities) == self.n_atoms:
            self._atom_opacities = atom_opacities
        else:
            raise ValueError("Number of opacities should be 1 or n_atoms")

        for it in range(self.n_atoms):
            self.atom_styles[it]["opacity"] = self._atom_opacities[it]
        return

    @property
    def atom_radii(self):
        return self._atom_radii

    @atom_radii.setter
    def atom_radii(self, atom_radii: list):

        if not isinstance(atom_radii, (list, float)):
            raise TypeError("atom_radii should be either list or float")
        elif isinstance(atom_radii, float):
            self._atom_radii = [
                atom_radii for _ in range(self.n_atoms)
            ]
        elif len(atom_radii) == self.n_atoms:
            self._atom_radii = atom_radii
        else:
            raise ValueError("Number of radii should be 1 or n_atoms")

        for it in range(self.n_atoms):
            self.atom_styles[it]["radius"] = self._atom_radii[it]

        return

    @property
    def atom_colours(self):
        return self._atom_colours

    @atom_colours.setter
    def atom_colours(self, atom_colours: list):

        if not isinstance(atom_colours, (list, str)):
            raise TypeError("atom_colours should be either list or str")
        elif isinstance(atom_colours, str):
            self._atom_colours = [
                atom_colours for it in range(self.n_atoms)
            ]
        elif len(atom_colours) == self.n_atoms:
            self._atom_colours = atom_colours
        else:
            raise ValueError("Number of colours should be 1 or n_atoms")

        for it in range(self.n_atoms):
            self.atom_styles[it]["color"] = self._atom_colours[it]

        return

    def __repr__(self) -> str:

        # Create atom specification
        atoms_spec = self.gen_atoms_spec()

        # Create model and add atoms to model
        model_str = "        var {} = viewer.addModel();\n".format(
            self.model_js_var
        )
        model_str += "            {}.addAtoms(eval({}));\n".format(
            self.model_js_var, atoms_spec
        )

        # Generate style dictionary
        set_styles = self.gen_set_style()

        # Merge in other style if present
        if len(self.extra_styles):
            set_styles = self.merge_styles(set_styles, self.extra_styles)

        # Print style dictionary
        for set_style in set_styles:
            model_str += "            {}.setStyle(".format(
                self.model_js_var
            )
            for ss in set_style:
                model_str += "{},".format(ss)
            model_str += ");\n"

        return model_str

    def gen_atoms_spec(self):
        """
        Creates dictionaries used to add molecules to 3Dmol.js viewer

        Resulting list of dictionaries is used as sole argument of js call to
        m.addAtoms();
        where m is defined as output of
        viewer.addModel();

        Parameters
        ----------
        coords : np.ndarray
            [n_atoms,3] array containing x, y, z coordinates of each atom
        labels : list
            Atom labels without indexing
        adjacency : np.ndarray
            [n_atoms, n_atoms] Adjacency matrix used to define bonds between
            atoms

        Returns
        -------
        list
            dictionaries, one per atom, describing atom label, position, and
            indices of other atoms bonded to that atom

        """

        n_bonds = np.sum(self.adjacency, axis=1)

        molecule = []
        for it, (xyz, label) in enumerate(zip(self.coords, self.labels_nn)):
            atdict = {}
            atdict["elem"] = label
            atdict["x"] = xyz[0]
            atdict["y"] = xyz[1]
            atdict["z"] = xyz[2]
            atdict["bonds"] = [
                jt for (jt, oz) in enumerate(self.adjacency[it]) if oz
            ]
            atdict["bondOrder"] = [1]*n_bonds[it]
            atdict["serial"] = it
            molecule.append(atdict)

        return molecule

    def gen_set_style(self):
        """
        Creates list of style dictionaries, one per atom, for 3dmol.js model

        Returns
        -------
            list
                style dictionaries, one per atom
        """

        set_style = [
            [
                {
                    "serial": "{:d}".format(it),
                },
                {
                    self.atom_rep[it]: style
                }
            ]
            for it, style in enumerate(self.atom_styles)
        ]

        return set_style

    @staticmethod
    def merge_styles(style_1, style_2):
        """
        Combines two lists of style dictionaries atom by atom
        This allows styles of a single atom to be combined, e.g.
        sphere + stick are combined to give a ball and stick representation

        Parameters
        ----------
        style_1 : list[dict]
            List of style dictionaries generated by `gen_set_style`
        style_2 : list[dict]
            List of style dictionaries generated by `gen_set_style`
        
        Returns
        -------
        list
            style dictionaries, one per atom
        """
        new_style = [
            [
                s1[0],
                dict(s1[1], **s2[1])
            ]
            for s1, s2 in zip(style_1, style_2)
        ]

        return new_style

class HtmlPage():
    """
    Object defining a single html file/page with given elements

    Parameters
    ----------
    header : list[str]
        lines to add to header section
    body : list[str]
        lines to add to body section
    footer : list[str]
        lines to add to footer section
    scripts : list[str]
        scripts to add to <script> section
    moljs : str
        location of 3dmol.js library
        Specify "live" to use online version at
        https://3Dmol.csb.pitt.edu/build/3Dmol-min.js
    
    Attributes
    ----------
    header : list[str]
        lines of header section
    body : list[str]
        lines of body section
    footer : list[str]
        lines of footer section
    """

    def __init__(self, header=[], body=[], footer=[], scripts=[],
                 moljs='live'):

        if moljs == 'live':
            string = '<script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js">' # noqa
            string += '</script>\n'

        for script in scripts:
            string += "<script>\n"
            string += script
            string += "</script>\n"

        self.header = header + [string]

        self.body = body

        self.footer = footer
        return

    def save(self, output="output.html"):
        """
        Saves string of current html page to file

        Parameters
        ----------
        output : str
            Name of output file
        """

        with open(output, "w") as oh:
            oh.write(str(self))

        return

    def __repr__(self):
        """
        String representation of current html page
        """
        string = ""

        for header in self.header:
            string += header

        string += '<body>\n'

        for body in self.body:
            string += body
            string += "\n"

        string += "</body>\n"

        return string
