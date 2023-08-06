import cro_validate.classes.definition_classes as Definitions
import cro_validate.classes.util_classes as Utils
from cro_validate.enum import DataType, ValidationMode
import cro_validate.util.definition_util as DefinitionUtil

def get(definition_or_name, version=Utils.Empty):
	"""
	Returns the :ref:`Definition` instance representing this definition. Use the
	returned Definition to retrieve all meta for this definition
	(name, data_type, etc.). Raises input error if Definition is not found.

	:param definition_or_name: Definition name to retrieve from the global index. For convenience, the :ref:`Definition` instance itself may be passed.
	:returns: The Definition instance loaded.
	:rtype: Definition
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.get(definition_or_name, version)


def exists(name):
	"""
	Returns True if the name is indexed, otherwise False.

	:param str name: Definition name to verify.
	:return: True if name exists, otherwise False.
	:rtype: bool
	:exception: Input error if definition not found.
	"""
	return Definitions.Index.exists(name)


def to_json_dict():
	"""
	Returns a dictionary representation of the definition index
	(name => Definition).

	:rtype: dict
	:return: A serializable dict representation of the definition index.
	"""
	return Definitions.Index.to_json_dict()


def from_json_dict(root):
	"""
	Instantiates definitions from a dictionary. See the format spec for
	more details.

	:return: None
	"""
	return Definitions.Index.from_json_dict(root)


def add_version(version, display_name=None):
	"""
	Adds a version to the index. See the versioning guide for more details.

	:param str version: Version tag to index definitions against.
	:param str display_name: A display name to associate with the version tag
	(for use with docs, etc.)
	:return: None
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.add_version(version, display_name)


def get_version_display_name(version):
	"""
	Retrieve the display name associated with the given version.

	:param str version: Version tag retrieve the display name for.

	:return: None
	:raises: Input error if version not found.
	"""
	return Definitions.Index.get_version_display_name(version)


def get_version_by_display_name(display_name):
	"""
	Retrieve the version by display name.

	:param str display_name: Display name to retrieve .

	:return: None
	:raises: Input error if display name not found.
	"""
	return Definitions.Index.get_version_by_display_name(display_name)


def list_versions():
	"""
	Retrieve the list of version strings.

	:return: None
	"""
	return Definitions.Index.list_versions()


def compare_versions(a, b):
	"""
	a < b => -1, a == b => 0, a > b => 1.

	:param str a: Version a.
	:param str a: Version b.

	:return: -1, 0, or 1.
	:raises: Input error if version a or b not found.
	"""
	return Definitions.Index.compare_versions(a, b)


def list_definition_versions(definition_or_name, include_identical=True):
	"""
	Retrive list of versions for a given definition.

	:param str definition_or_name: Definition name or object to retrieve versions for.
	:param str include_identical: Include versions with no changes in the result.

	:return: List of version strings.
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.list_definition_versions(definition_or_name, include_identical)


def definition_has_version(definition_or_name, version):
	"""
	Returns True if definition has changes in given version.

	:param str definition_or_name: Definition name or object to check.
	:param str version: Version to check.

	:return: True if version has changes, False otherwise.
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.definition_has_version(definition_or_name, version)


def get_definition_base_version(definition_or_name):
	"""
	Returns first version in the version index for the given definition.

	:param str definition_or_name: Definition name or object.

	:return: Base version str for definition.
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.get_definition_base_version(definition_or_name)


def get_definition_final_version(definition_or_name):
	"""
	Returns first version in the version index for the given definition.

	:param str definition_or_name: Definition name or object.

	:return: Base version str for definition.
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.get_definition_final_version(definition_or_name)


def get_definition_previous_version(definition_or_name, version):
	"""
	Returns version previous to the given version.

	:param str definition_or_name: Definition name or object.
	:param str version: Version to reference.

	:return: Previous version string, relative to given version.
	:raises: Input error if definition not found or previous version not found.
	"""
	return Definitions.Index.get_definition_previous_version(definition_or_name, version)


def get_latest_version():
	"""
	Returns latest version in the index.

	:return: Latest indexed version.
	"""
	return Definitions.Index.get_latest_version()


def get_first_version():
	"""
	Returns first version in the index. Excludes special version "base" (i.e.
	the first user-specified version in the index).

	:return: First user-specified version.
	"""
	return Definitions.Index.get_first_version()


def version_exists(version):
	"""
	Returns True if the given version is indexed.

	:return: True if version exists, otherwise False.
	"""
	return Definitions.Index.version_exists(version)


def register_data_type_rule(data_type, rule, exceptions=[]):
	"""
	Register global validation rule to execute against all definitions with
	the given data type, minus the exceptions in the exceptions list.

	:param Int data_type: DataType value to compare against.
	:param Rule rule: Rule object to execute during definition validation.
	:param list exceptions: List of definition names to exclude from executing this rule against.

	:return: None
	"""
	return Definitions.Index.register_data_type_rule(data_type, rule, exceptions)


def register_data_format_rule(data_format, rule, exceptions=[]):
	"""
	Register global validation rule to execute against all definitions with
	the given data format, minus the exceptions in the exception list.

	:param Int data_type: User-specified format value to compare against.
	:param Rule rule: Rule object to execute during definition validation.
	:param list exceptions: List of definition names to exclude from executing this rule against.

	:return: None
	"""
	return Definitions.Index.register_data_format_rule(data_format, rule, exceptions)


def register_definition(
 			name=Utils.Empty,
			aliases=Utils.Empty,
			description=Utils.Empty,
			data_type=Utils.Empty,
			data_format=Utils.Empty,
			default_value=Utils.Empty,
			examples=Utils.Empty,
			nullable=Utils.Empty,
			deprecated=Utils.Empty,
			internal=Utils.Empty,
			rules=Utils.Empty,
			base_version=Utils.Empty,
			final_version=Utils.Empty,
			versions=Utils.Empty,
			meta=Utils.Empty
		):
	"""
	Register a definition.

	:param str name: Indexed name used to access and refer to this definition.
	:param list aliases: List of strings which will be indexed as aliases.
	:param str description: A description for use with docs, help, etc.
	:param DataType data_type: The DataType of this definition (Integer, etc.).
	:param data_format int: User-defined constant representing the expected format.
	:param list examples: List of examples of valid values (for use with docs, etc.).
	:param default_value: Value to use during validation, initialization, etc. by default.
	:param nullable: Values can be None when True, otherwise an input error will be raised during validation on None.
	:param bool deprecated: For use with docs, etc. Does not affect validation.
	:param internal: For use with docs, etc. Does not affect validation.
	:param list rules: List of Rule instances to execute during validation.
	:param str base_version: Initial version of this definition (will be unavailable if earlier versions requested).
	:param str final_version: Final version of this definition (unavailable if later versions requested).
	:param dict versions: Dict of versioning info. See version guide for more info.
	:param meta: User-specified object of meta data to store with this definition.
	:return: None
	"""
	result = Definitions.Index.register_definition(
			name=name,
			aliases=aliases,
			description=description,
			data_type=data_type,
			data_format=data_format,
			default_value=default_value,
			examples=examples,
			nullable=nullable,
			deprecated=deprecated,
			internal=internal,
			rules=rules,
			base_version=base_version,
			versions=versions,
			meta=meta
		)
	return result


def ensure_alias(name, alias):
	"""
	If alias doesn't exist, create it.

	:param str name: Name of definition to alias (must exist).
	:param str alias: Alias to assign.

	:return None:
	"""
	Definitions.Index.ensure_alias(name, alias)


def list_definitions():
	"""
	Retrieve list of definitions.

	:return list: Return list of definitions (unordered).
	"""
	results = Definitions.Index.list_definitions()
	return results


def validate_input(
			definition_or_name,
			value,
			field_fqn=None,
			field_name=None,
			version=Utils.Empty,
			**rules_kw
		):
	"""
	Raises input error on validation fail. Some validation rules transform the
	data, and these transforms may be specific in context of input/output. Case
	sensitivity is assumed to be normalized during output, and will be normalized
	for input validation. See the validation guide for more info.

	:param definition_or_name: Definition instance or definition name.
	:param value: Input to validate.
	:param str field_fqn: The fully qualified name for the field (used for exception handling).
	:param str field_name: The field name (for error/exception handling).
	:param str version: Version of definition to select to validate against.
	:param rules_kw: All additional named args will be passed to rules as they are executed.
 	:return None:
	:raises: Raises input error on validation fail.
	"""
	results = Definitions.Index.validate(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			version,
			ValidationMode.Input,
			**rules_kw
		)
	return results


def validate_output(
			definition_or_name,
			value,
			field_fqn=None,
			field_name=None,
			version=Utils.Empty,
			**rules_kw
		):
	"""
	Raises input error on validation fail. Some validation rules transform the
	data, and these transforms may be specific in context of input/output. Case
	sensitivity is assumed to be normalized during output, and will be normalized
	for input validation. See the validation guide for more info.

	:param definition_or_name: Definition instance or definition name.
	:param value: Input to validate.
	:param str field_fqn: The fully qualified name for the field (used for exception handling).
	:param str field_name: The field name (for error/exception handling).
	:param str version: Version of definition to select to validate against.
	:param rules_kw: All additional named args will be passed to rules as they are executed.
 	:return None:
	:raises: Raises input error on validation fail.
	"""
	results = Definitions.Index.validate(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			version,
			ValidationMode.Output,
			**rules_kw
		)
	return results


def mutate_input_version(
			definition_or_name,
			value,
			src_version,
			target_version,
			field_fqn=None,
			field_name=None,
			**rules_kw
		):
	"""
	Convert from one version to another.

	:param definition_or_name: Definition instance or definition name.
	:param value: The value to mutate.
	:param str src_version: The input version (format of value).
	:param str target_version: The version to convert to.
	:param str field_fqn: The fully qualified name for the field (used for exception handling).
	:param str field_name: The field name (for error/exception handling).
	:param rules_kw: All additional named args will be passed to rules as they are executed.
	"""
	results = Definitions.Index.mutate_input_version(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			src_version,
			target_version,
			**rules_kw
		)
	return results


def instantiate(
			fqn,
			field_name,
			definition_or_name,
			version=Utils.Empty,
			validate=True,
			rules_kw={},
			**initial_values
		):
	"""
	Create value instance based on data definition.

	:param definition_or_name: Definition instance or definition name.
	:param str field_name: The field name (for error/exception handling).
	:param str version: Version to instantiate.
	:parma bool validate: Validate as input if True, skip otherwise.
	:param rules_kw: All additional named args will be passed to rules as they are executed.
	:return: Return instantiated value.
	"""
	result = Definitions.Index.instantiate(
			fqn,
			field_name,
			definition_or_name,
			version,
			validate,
			rules_kw,
			**initial_values
		)
	return result


def recurse_definition(
			definition,
			fqn,
			value,
			cb,
			case_sensitive=True,
			ignore_unknown_inputs=False,
			version=Utils.Empty,
			**kw
		):
	"""
	Recursively visit the fields of a given value based on given definition.

	:param definition: Definition instance or definition name.
	:param str fqn: The fully qualified name for the field (used for exception handling).
	:param value: Value to recurse.
	:param cb: Callable (fucntion or class implementing __call__) to use as callback.
	:param bool case_sensitive: Field name matches are case sensitive when True.
	:param bool ignore_unknown_inputs: If an unknown field is encountered, an input error is raised unless this value is True.
	:param str version: Version of definition to recurse against.
	:param kw: Named args will be passed to callback.
	:return None:
	"""
	return DefinitionUtil.recurse_definition(
				definition,
				fqn,
				None,
				None,
				value,
				cb,
				case_sensitive,
				ignore_unknown_inputs,
				version,
				**kw
			)


def set_default_version(default_version):
	"""
	The default version is "base". Calling set_default_version will cause any calls
	accepting a version argument with the version arg omitted to use the default_version.

	:param str default_version: Version to use as default for calls where the version is not specified.
	:return None:
	"""
	Definitions.Index.set_default_version(default_version)


def clear():
	"""
	Reset definition index (remove all definitions).

	:return None:
	"""
	Definitions.Index.clear()