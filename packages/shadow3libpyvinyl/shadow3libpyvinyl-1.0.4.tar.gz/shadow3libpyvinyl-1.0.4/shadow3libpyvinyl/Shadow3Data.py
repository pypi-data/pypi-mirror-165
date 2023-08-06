

# treat the Shadow.Beam() data as libpyvinyl data. Two file formats: raw format (original shadow3) and openPMD format.

from libpyvinyl.BaseData import BaseData
from libpyvinyl.BaseFormat import BaseFormat


import Shadow
from shadow3libpyvinyl.openPMD import loadShadowOpenPMD, saveShadowToHDF

class Shadow3Data(BaseData):
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):

        expected_data = {}
        expected_data["nrays"] = None
        expected_data["rays"] = None


        super().__init__(key,
                         expected_data,
                         data_dict,
                         filename,
                         file_format_class,
                         file_format_kwargs)

    @classmethod
    def supported_formats(self):
        format_dict = {}
        ### DataClass developer's job start
        self._add_ioformat(format_dict, Shadow3BeamFormat)
        self._add_ioformat(format_dict, Shadow3OpenPMDFormat)
        ### DataClass developer's job end
        return format_dict

    def duplicate(self):

        return Shadow3Data(
                 self.key,
                 data_dict={"nrays": self.get_data()["nrays"], "rays": self.get_data()["rays"].copy()},
                 filename=self.filename,
                 file_format_class=self.file_format_class,
                 file_format_kwargs=self.file_format_kwargs)



class Shadow3BeamFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "shadow3beam_raw"
        desciption = "Beam format (raw) for Shadow3Beam"
        file_extension = ".dat"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        print(">>>>>>>>>>>>>>>>>>>>>>>>> reading RAW....")
        try:
            beam = Shadow.Beam()
            beam.load(filename)
            return {"nrays": beam.nrays(), "rays": beam.rays}
        except:
            raise Exception("Error loading file %s" % (filename) )

    @classmethod
    def write(cls, object: Shadow3Data, filename: str, key: str = None):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> writing RAW")
        b = Shadow.Beam(N=object.get_data()["nrays"])
        b.rays = object.get_data()["rays"]
        b.write(filename)
        print("File %s with shadow3 beam (raw format) written to disk." % filename)


    @staticmethod
    def direct_convert_formats():
        # TO DO...
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []

class Shadow3OpenPMDFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "shadow3beam_openPMD"
        desciption = "Beam format (openPMD) for Shadow3Beam"
        file_extension = ".h5"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        print(">>>>>>>>>>>>>>>>>>>>>>>>> reading openPMD....")
        try:
            beam = loadShadowOpenPMD(filename)
            return {"nrays": beam.nrays(), "rays": beam.rays}
        except:
            raise Exception("Error loading file %s" % (filename) )

    @classmethod
    def write(cls, object: Shadow3Data, filename: str, key: str = None):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> writing openPMD")
        b = Shadow.Beam(N=object.get_data()["nrays"])
        b.rays = object.get_data()["rays"]
        saveShadowToHDF(b, filename=filename, workspace_units_to_cm=100.0)
        print("File %s with shadow3 beam (openPMD format) written to disk." % filename)


    @staticmethod
    def direct_convert_formats():
        # TODO...
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []
if __name__ == "__main__":


    # # Test if the definition works
    # data = Shadow3Data(key="test")
    # print(data.key)
    # print(data.expected_data)
    #
    # #
    # # add test data
    # #
    # b = Shadow.Beam()
    # b.genSource( Shadow.Source() )
    # data.set_dict( {"nrays":b.nrays(), "rays":b.rays})
    #
    # # print(data.get_data())
    #
    #
    # # file i/o
    #
    # Shadow3Data.list_formats()
    #
    # # write RAW
    # data.write('tmp11.dat', Shadow3BeamFormat)
    #
    # # read RAW
    # loaded_data = Shadow3Data(key="test_data",
    #                         data_dict=None,
    #                         filename=None,
    #                         file_format_class=None,
    #                         file_format_kwargs=None
    #                         )
    # loaded_data.set_file("tmp11.dat", Shadow3BeamFormat)
    # print(loaded_data.get_data()["nrays"], loaded_data.get_data()["rays"].shape)
    #
    # # write OpenPMD
    # data.write('tmp11.h5', Shadow3OpenPMDFormat)
    #
    # # read OpenPMD
    # loaded_data = Shadow3Data(key="test_data",
    #                         data_dict=None,
    #                         filename=None,
    #                         file_format_class=None,
    #                         file_format_kwargs=None
    #                         )
    # loaded_data.set_file("tmp11.h5", Shadow3OpenPMDFormat)
    # print(loaded_data.get_data()["nrays"], loaded_data.get_data()["rays"].shape)

    #
    # copy/duplicate data
    #
    b = Shadow.Beam()
    b.genSource( Shadow.Source() )
    data = Shadow3Data(key="test")
    data.set_dict( {"nrays":b.nrays(), "rays":b.rays})

    print(data.get_data())

    data2 = data.duplicate()

    rays = data.get_data()["rays"]
    rays *= 0

    print(data.get_data())
    print(data2.get_data())




