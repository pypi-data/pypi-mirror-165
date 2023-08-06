# generalfile
Easily manage files cross platform.

This package and 3 other make up [ManderaGeneral](https://github.com/ManderaGeneral).

## Information
| Package                                                      | Ver                                            | Latest Release        | Python                                                                                                                   | Platform        |   Lvl | Todo                                                    | Cover   |
|:-------------------------------------------------------------|:-----------------------------------------------|:----------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|------:|:--------------------------------------------------------|:--------|
| [generalfile](https://github.com/ManderaGeneral/generalfile) | [2.5.8](https://pypi.org/project/generalfile/) | 2022-09-01 06:56 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu |     1 | [4](https://github.com/ManderaGeneral/generalfile#Todo) | 73.1 %  |

## Contents
<pre>
<a href='#generalfile'>generalfile</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                   | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/send2trash'>send2trash</a>   | <a href='https://pypi.org/project/appdirs'>appdirs</a>   | <a href='https://pypi.org/project/pandas'>pandas</a>   | <a href='https://pypi.org/project/dill'>dill</a>   |
|:--------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|
| `pip install generalfile` | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    | Yes                                                |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/__init__.py#L1'>Module: generalfile</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/errors.py#L6'>Class: CaseSensitivityError</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L109'>Class: ConfigFile</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L139'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L94'>Method: get_custom_serializers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L102'>Method: get_field_dict_serializable</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L168'>Method: halt_getattr</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L15'>Method: read_hook_post</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L14'>Method: read_hook_pre</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L148'>Method: safe_equals</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L56'>Method: write_config</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L17'>Method: write_hook_post</a> <b>(Untested)</b>
│  └─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/configfile.py#L16'>Method: write_hook_pre</a> <b>(Untested)</b>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/errors.py#L10'>Class: InvalidCharacterError</a>
└─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path.py#L20'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path.py#L20'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L32'>Method: absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_lock.py#L123'>Method: as_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/optional_dependencies/path_cfg.py#L13'>Property: cfg</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L426'>Method: contains</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L97'>Method: copy</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L158'>Method: copy_to_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L237'>Method: create_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L311'>Method: delete</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L343'>Method: delete_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L216'>Method: empty</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L268'>Method: encode</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L94'>Method: endswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L204'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L24'>Method: from_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L40'>Method: get_active_venv</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L283'>Method: get_cache_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L399'>Method: get_differing_files</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L293'>Method: get_lock_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L302'>Method: get_lock_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L25'>Method: get_parent_package</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L32'>Method: get_parent_repo</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L18'>Method: get_parent_venv</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L255'>Method: get_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L59'>Method: is_absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L174'>Method: is_file</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L180'>Method: is_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L381'>Method: is_identical</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L10'>Method: is_package</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L66'>Method: is_relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L14'>Method: is_repo</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L186'>Method: is_root</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_envs.py#L6'>Method: is_venv</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_lock.py#L114'>Method: lock</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L261'>Method: match</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L73'>Method: mirror_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L166'>Method: move</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L153'>Method: name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L247'>Method: open_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L31'>Method: open_operation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L446'>Method: pack</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L145'>Method: parts</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/optional_dependencies/path_pickle.py#L12'>Property: pickle</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L64'>Method: read</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L42'>Method: relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L120'>Method: remove_end</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L103'>Method: remove_start</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L73'>Method: rename</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L195'>Method: root</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L136'>Method: same_destination</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_scrub.py#L10'>Method: scrub</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L360'>Method: seconds_since_creation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L368'>Method: seconds_since_modified</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L274'>Method: set_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L375'>Method: size</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_diagram.py#L20'>Method: spawn_children</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_diagram.py#L11'>Method: spawn_parents</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/optional_dependencies/path_spreadsheet.py#L13'>Property: spreadsheet</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L85'>Method: startswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L169'>Method: stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L201'>Method: suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L245'>Method: suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/optional_dependencies/path_text.py#L12'>Property: text</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L16'>Method: to_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L332'>Method: trash</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L352'>Method: trash_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L185'>Method: true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L465'>Method: unpack</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_diagram.py#L7'>Method: view_paths</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L160'>Method: with_name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L176'>Method: with_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L209'>Method: with_suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L252'>Method: with_suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_strings.py#L192'>Method: with_true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L228'>Method: without_file</a>
   └─ <a href='https://github.com/ManderaGeneral/generalfile/blob/e054043/generalfile/path_bases/path_operations.py#L51'>Method: write</a>
</pre>

## Todo
| Module                                                                                                                                               | Message                                                                                                                                                                                   |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional_dependencies/path_spreadsheet.py#L1'>path_spreadsheet.py</a> | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional_dependencies/path_spreadsheet.py#L112'>Support DataFrame and Series with spreadsheet.append()</a> |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_bases/path_lock.py#L1'>path_lock.py</a>                          | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_bases/path_lock.py#L12'>Lock the optional extra paths.</a>                                            |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L27'>Binary extension.</a>                                                                         |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/configfile.py#L1'>configfile.py</a>                                   | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/configfile.py#L117'>Handle custom serializers within iterable for ConfigFile.</a>                          |

<sup>
Generated 2022-09-01 06:56 CEST for commit <a href='https://github.com/ManderaGeneral/generalfile/commit/e054043'>e054043</a>.
</sup>
