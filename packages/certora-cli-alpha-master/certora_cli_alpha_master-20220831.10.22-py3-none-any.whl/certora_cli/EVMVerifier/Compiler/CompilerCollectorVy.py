from pathlib import Path
from typing import Dict, Any

from EVMVerifier.Compiler.CompilerCollector import CompilerCollector, CompilerLang
from Shared.certoraUtils import Singleton


class CompilerLangVy(CompilerLang, metaclass=Singleton):
    """
    [CompilerLang] for Vyper.
    """
    _compiler_name: str = "vyper"

    @property
    def name(self) -> str:
        return "Vyper"

    @property
    def compiler_name(self) -> str:
        return self._compiler_name

    @staticmethod
    def normalize_func_hash(func_hash: str) -> str:
        try:
            return hex(int(func_hash, 16))
        except ValueError:
            raise Exception(f'{func_hash} is not convertible to hexadecimal')

    @staticmethod
    def normalize_file_compiler_path_name(file_abs_path: str) -> str:
        assert file_abs_path.startswith('/'), f'expected {file_abs_path} to begin with forwardslash'
        return file_abs_path[1:]

    @staticmethod
    def normalize_deployed_bytecode(deployed_bytecode: str) -> str:
        assert deployed_bytecode.startswith("0x"), f'expected {deployed_bytecode} to have hexadecimal prefix'
        return deployed_bytecode[2:]

    @staticmethod
    def get_contract_def_node_ref(contract_file_ast: Dict[int, Any], contract_file: str, contract_name: str) -> \
            int:
        # in vyper, "ContractDefinition" is "Module"
        contract_def_refs = list(filter(
            lambda node_id: contract_file_ast[node_id].get("ast_type") == "Module" and
            contract_file_ast[node_id].get("name") == contract_file, contract_file_ast))
        assert len(contract_def_refs) != 0, \
            f'Failed to find a "Module" ast node id for the file {contract_file}'
        assert len(contract_def_refs) == 1, f'Found multiple "Module" ast node ids for the same file' \
            f'{contract_file}: {contract_def_refs}'
        return contract_def_refs[0]

    @staticmethod
    def get_standard_json_filename(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}"


class CompilerCollectorVy(CompilerCollector):

    @property
    def compiler_name(self) -> str:
        return self.smart_contract_lang.compiler_name

    @property
    def smart_contract_lang(self) -> CompilerLangVy:
        return CompilerLangVy()

    @property
    def compiler_version(self) -> str:
        return "vyper"  # TODO implement to return a valid version
