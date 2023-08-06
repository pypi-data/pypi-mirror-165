

# treat the Shadow.Source and Shadow.OE data as libpyvinyl data (not used, as they are in parameters)

from libpyvinyl.BaseData import BaseData
from libpyvinyl.BaseFormat import BaseFormat
import inspect
import numpy



from libpyvinyl.BaseData import DataCollection
import Shadow

class Shadow3GData(BaseData):
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):

        expected_data = {}
        expected_data["DUMMY"] = None


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
        self._add_ioformat(format_dict, Shadow3GfileFormat)
        ### DataClass developer's job end
        return format_dict


class Shadow3GfileFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "Gfile"
        desciption = "Gfile format for Shadow3GData"
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
        flag = cls.shadow3_file_type(filename)
        if flag == 0:
            oe0 = Shadow.Source()
            oe0.load(filename)
            return oe0.to_dictionary()
        elif flag == 1:
            oe1 = Shadow.OE()
            oe1.load(filename)
            return oe1.to_dictionary()
        else:
            raise Exception("Error loading file %s (flag=%d)" % (filename, flag) )

    @classmethod
    def write(cls, object: Shadow3GData, filename: str, key: str = None):


        dict1 = object.get_data()
        keys = dict1.keys()
        if 'F_WIGGLER' in keys:
            shadow_object = Shadow.Source()
            print(">>>>>>>>>>>> source")
        elif 'F_GRATING' in keys:
            shadow_object = Shadow.OE()
            print(">>>>>>>>>>>> oe")
        else:
            raise Exception("Mismatch data")

        i_list = cls.__get_valiable_list(shadow_object)

        for name in i_list:
            try:
                value = dict1[name]
                if isinstance(value, str):
                    value = bytes(value, 'UTF-8')
                elif isinstance(value, numpy.ndarray):
                    for list_item in value:
                        if isinstance(list_item, str):
                            list_item = bytes(list_item, 'UTF-8')
                setattr(shadow_object, name, value)
            except:
                raise Exception("Error setting parameters name %s" % name)

        shadow_object.write(filename)

        if key is None:
            original_key = object.key
            key = original_key + "_to_Shadow3GfileFormat"
            return object.from_file(filename, cls, key)
        else:
            return object.from_file(filename, cls, key)

    @staticmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []

    @staticmethod
    def shadow3_file_type(filename):
        with open(filename) as f:
            if 'F_WIGGLER' in f.read():
                return 0
        with open(filename) as f:
            if 'F_GRATING' in f.read():
                return 1
        return -1

    @staticmethod
    def __get_valiable_list(object1):
        """
        returns a list of the Shadow.Source or Shadow.OE variables
        """
        mem = inspect.getmembers(object1)
        mylist = []
        for i,var in enumerate(mem):
            if var[0].isupper():
                mylist.append(var[0])
        return(mylist)


if __name__ == "__main__":


    # Test if the definition works
    data = Shadow3GData(key="test")
    print(data.key)
    print(data.expected_data)

    # # see: libpyvinyl/tests/unit/test_BaseData.py

    # Shadow data


    oe0 = Shadow.Source()
    oe0_dict = oe0.to_dictionary()

    shadow_data0 = Shadow3GData(key="oe0")
    shadow_data0.set_dict(oe0_dict)
    # print(shadow_data0.get_data())

    oe1 = Shadow.OE()
    oe1_dict = oe1.to_dictionary()
    # print(oe0_dict)

    shadow_data1 = Shadow3GData(key="oe1")
    shadow_data1.set_dict(oe1_dict)
    # print(shadow_data.get_data())

    print(shadow_data0.get_data())
    print(shadow_data1.get_data())

    shadow_beamline = DataCollection(shadow_data0, shadow_data1)
    print(shadow_beamline["oe0"].get_data())
    print(shadow_beamline["oe1"].get_data())

    print(len(shadow_beamline))
    print(shadow_beamline.to_list())

    # file i/o
    Shadow3GData.list_formats()
    oe0 = Shadow.Source()
    oe0.write("tmp0.dat")
    test_data = Shadow3GData(key="test_data")
    test_data.set_file("tmp0.dat", Shadow3GfileFormat)
    # print(test_data.get_data())

    oe1 = Shadow.OE()
    oe1.write("tmp1.dat")
    test_data = Shadow3GData(key="test_data")
    test_data.set_file("tmp1.dat", Shadow3GfileFormat)
    test_data.write('tmp11.dat', Shadow3GfileFormat)
    tmp = Shadow.OE()
    tmp.load('tmp11.dat')
    # print(test_data.get_data())

