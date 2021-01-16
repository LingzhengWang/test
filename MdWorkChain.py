from aiida.engine import WorkChain
from aiida.orm import StrucureData
from ecint.preprocessor.utils import inspect_node
class MdWorkChain(WorkChain):
    def define(cls,spec):
        super(Cp2kWorkChain,cls).define(spec)
        spec.input_namespace('structures',valid_type=StructureData,dynamic=True)
        spec.input('machine', default=default_cp2k_large_machine, valid_type=dict, required=False, non_db=True)
        spec.outline(
                cls.check_config_machine,
                cls.submit_cp2k,
                cls.inspect_cp2k,
        )
        spec.output()
        spec.output()

    def submit_cp2k(self):
        class Cp2kInputSets():
            def _init_(structure,config,kind_section):
                self.structure=structure
                self.config=config
                self.kind_section=kind_section
        inp = Cp2kInputSets(structure=self.ctx.reactant,
                            config=self.ctx.config,
                            kind_section=self.inputs.kind_section)
        for image_index in range(len(self.inputs.structures)):
            inp.add_config({
                'MOTION':{
                    'BAND':{
                        'REPLACE':[
                            {'COORD_FILE_NAME': f'image_{image_index}.xyz'}]
                     }
                }
            })
        class Cp2kPreprocessor():
            def _init_(inp,se)
        pre = Cp2kPreprocessor(inp, self.ctx.machine)
        builder = pre.builder
        builer.cp2k.file = self.submit(builder)
        self.to_context(cp2k_workchain_node)
    def inspect_cp2k(self):
        inspect_node(self.ctx.cp2k_workchain)