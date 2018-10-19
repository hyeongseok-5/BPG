import BPG


class SubLevel2(BPG.PhotonicTemplateBase):
    def __init__(self, temp_db,
                 lib_name,
                 params,
                 used_names,
                 **kwargs,
                 ):
        """ Class for generating a single mode waveguide shape in Lumerical """
        BPG.PhotonicTemplateBase.__init__(self, temp_db, lib_name, params, used_names, **kwargs)

    @classmethod
    def get_params_info(cls):
        return dict(
        )

    @classmethod
    def get_default_param_values(cls):
        return dict(
        )

    def draw_layout(self):
        """ Specifies the creation of the lumerical shapes """
        circ = BPG.photonic_objects.PhotonicRound(
            layer='SI',
            resolution=self.grid.resolution/100,
            center=(40, 30),
            rout=10,
            rin=5,
            # theta0=45,
            # theta1=60,
            unit_mode=False
        )
        self.add_round(circ)

        self.add_rect(
            layer='SI',
            coord1=(10, 10),
            coord2=(20, 24),
        )

        self.add_rect(
            layer='POLY',
            coord1=(-100, -100),
            coord2=(-50, -70),
        )

        self.add_polygon(
            layer='POLY',
            points=[(0, 0), (10, 0), (10, 5), (0, 5)]
        )

        self.add_polygon(
            layer='SI',
            points=[(0, 0), (20, 0), (20, 10)]
        )

        self.add_polygon(
            layer='SI',
            points=[(30, 0), (40, 10), (50, 0), (40, -10)]
        )

        # This rectangle should disappear as it is minimum width
        self.add_rect(
            layer='SI',
            x_span=self.photonic_tech_info.max_width('SI'),
            y_span=self.photonic_tech_info.min_width('SI'),
            center=(40, -10)
        )
        # This rectangle should NOT disappear as it is minimum width + eps
        self.add_rect(
            layer='SI',
            x_span=self.photonic_tech_info.max_width('SI'),
            y_span=self.photonic_tech_info.min_width('SI') + self.grid.resolution,
            center=(40, -20)
        )

        self.add_photonic_port(
            name='Port1',
            center=(-10, -10),
            orient='R0',
            width=1,
            layer='SI'
        )

        self.add_photonic_port(
            name='Port2',
            center=(-10, -10),
            orient='R0',
            width=1,
            layer='POLY'
        )

        has_failed = False
        try:
            self.photonic_tech_info.min_width('LayerDoesNotExist')
        except ValueError:
            has_failed = True

        assert has_failed is True


def test_dataprep():
    """
    Unit Test
    """
    # Load a previous BPG Project if it exists, otherwise create a new one
    local_dict = locals()
    if 'prj' not in local_dict:
        print('creating BAG project')
        bprj = BPG.PhotonicBagProject()

    else:
        print('loading BAG project')
        bprj = local_dict['bprj']

    spec_file = 'BPG/tests/specs/dataprep_debug_specs.yaml'
    plm = BPG.PhotonicLayoutManager(bprj, spec_file, verbose=True)
    plm.generate_flat_gds()
    plm.dataprep()


if __name__ == '__main__':
    test_dataprep()
