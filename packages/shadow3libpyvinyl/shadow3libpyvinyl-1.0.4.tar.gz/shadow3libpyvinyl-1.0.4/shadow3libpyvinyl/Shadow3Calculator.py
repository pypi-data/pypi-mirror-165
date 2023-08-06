from libpyvinyl.BaseCalculator import BaseCalculator

from libpyvinyl.Parameters.Collections import CalculatorParameters, Parameter

from libpyvinyl.Parameters.Parameter import Parameter
import Shadow
import inspect
import numpy

from typing import Union
from libpyvinyl.BaseData import DataCollection
from shadow3libpyvinyl.Shadow3Data import Shadow3Data

class Shadow3Calculator(BaseCalculator):
    def __init__(
        self,
        name: str,
        input: Union[DataCollection, list, Shadow3Data],
        output_keys: Union[list, str] = ["shadow3_libpyvinyl_result"],
        output_data_types=[Shadow3Data],
        output_filenames: Union[list, str] = [],
        instrument_base_dir="./",
        calculator_base_dir="Shadow3Calculator",
        parameters=None,
    ):
        """A python object calculator example"""
        super().__init__(
            name,
            input,
            output_keys,
            output_data_types=output_data_types,
            output_filenames=output_filenames,
            instrument_base_dir=instrument_base_dir,
            calculator_base_dir=calculator_base_dir,
            parameters=parameters,
        )

    def init_parameters(self):
        parameters = CalculatorParameters()
        self.parameters = parameters

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

    def backengine(self):

        d1 = self.parameters.to_dict()

        d1_keys_list = []
        d1_keys_oe = []
        for key in d1.keys():
            pp = key.find('.')
            d1_keys_list.append(key[1+pp:])
            substr = key[2:pp]
            d1_keys_oe.append(int(substr))


        print(d1_keys_list, d1_keys_oe)


        found_optical_elements = []
        for i in range(1,501):
            if ("oe%d.DUMMY" % i) in d1.keys():
                found_optical_elements.append(i)

        number_of_optical_elements = len(found_optical_elements)
        print("number of optical elements", number_of_optical_elements, len(found_optical_elements), found_optical_elements)

        if 0 in d1_keys_oe: # source input found
            oe0 = Shadow.Source()
            for i in range(len(d1_keys_list)):
                if d1_keys_oe[i] == 0:
                    name = d1_keys_list[i]
                    try:
                        value = self.parameters["oe0."+name].value
                        if isinstance(value, str):
                            value = bytes(value, 'UTF-8')
                        setattr(oe0, name, value)
                    except:
                        raise Exception("Error setting parameters name %s" % name)

            beam = Shadow.Beam()
            beam.genSource(oe0)

        else:

            if self.input is not None:
                beam = Shadow.Beam(N=self.input.get_data()["nrays"])
                beam.rays = self.input.get_data()["rays"]
            else:
                raise Exception("Source parameters not found")


        if number_of_optical_elements > 0:
            for noe in found_optical_elements:
                oe_i = Shadow.OE()
                for j in range(len(d1_keys_list)):
                    if d1_keys_oe[j] == noe:
                        name = d1_keys_list[j]
                        try:
                            value = self.parameters["oe%d.%s" % (noe, name)].value
                            if isinstance(value, str):
                                value = bytes(value, 'UTF-8')
                            elif isinstance(value, numpy.ndarray):
                                for list_item in value:
                                    if isinstance(list_item, str):
                                        list_item = bytes(list_item, 'UTF-8')
                            setattr(oe_i, name, value)
                        except:
                            raise Exception("Error setting parameters name %s" % name)

                beam.traceOE(oe_i, noe)

        key = self.output_keys[0]
        output_data = self.output[key]
        output_data.set_dict({"nrays": beam.nrays(), "rays": beam.rays})
        return self.output


def get_calculator_parameters(oe0=None, oe_list=[]):

    parameters = CalculatorParameters()

    #
    # add source
    #
    if oe0 is not None:
        # oe0 = Shadow.Source()
        oe0_dict = oe0.to_dictionary()

        for key in oe0_dict.keys():
            print(key,oe0_dict[key], type(oe0_dict[key]))
            p = Parameter("oe0.%s" % key, "")
            if isinstance(oe0_dict[key], bytes):
                p.value = str(oe0_dict[key])
            else:
                p.value = oe0_dict[key]
            parameters.add(p)


    for i in range(len(oe_list)):
        n = i+1
        oe = oe_list[i]
        # oe = Shadow.OE()
        oe_dict = oe.to_dictionary()

        for key in oe_dict.keys():
            # print(key,oe0_dict[key], type(oe0_dict[key]))
            p = Parameter("oe%d.%s" % (n, key), "")
            if isinstance(oe_dict[key], bytes):
                p.value = str(oe_dict[key])
            else:
                p.value = oe_dict[key]
            parameters.add(p)

    return parameters

if __name__ == "__main__":



    calculator = Shadow3Calculator("test_run", # name: str,
        None, # input: Union[DataCollection, list, Shadow3Data],
        output_keys = ["shadow3_libpyvinyl_result"], # output_keys: Union[list, str] = ["shadow3_libpyvinyl_result"],
        output_data_types=[Shadow3Data],
        output_filenames = [], # output_filenames: Union[list, str] = [],
        instrument_base_dir="./",
        calculator_base_dir="Shadow3Calculator",
        parameters=None,)

    calculator.parameters = get_calculator_parameters(oe0=Shadow.Source(),oe_list=[Shadow.OE()])
    calculator.backengine()

    print(calculator.data)
    print(calculator.data.get_data())

    ### Plot results using ShadowTools
    try:
        from srxraylib.plot.gol import set_qt
        set_qt()
    except:
        pass
    beam = Shadow.Beam(N=calculator.data.get_data()["nrays"])
    beam.rays = calculator.data.get_data()["rays"]
    Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space")
