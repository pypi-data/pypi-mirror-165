# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set


TEXT: str = "text"
JSON: str = "json"
SARIF: str = "sarif"


class ProfileOutput(enum.Enum):
    TRACE_EVENT: str = "trace_event"
    COLD_START_PHASES: str = "cold_start_phases"
    INCREMENTAL_UPDATES: str = "incremental_updates"
    TAINT: str = "taint"
    INDIVIDUAL_TABLE_SIZES: str = "individual_table_sizes"
    TOTAL_SHARED_MEMORY_SIZE_OVER_TIME: str = "total_shared_memory_size_over_time"
    TOTAL_SHARED_MEMORY_SIZE_OVER_TIME_GRAPH: str = (
        "total_shared_memory_size_over_time_graph"  # noqa B950
    )

    def __str__(self) -> str:
        return self.value


class MissingFlowsKind(str, enum.Enum):
    OBSCURE: str = "obscure"
    TYPE: str = "type"


@dataclass(frozen=True)
class CommandArguments:
    local_configuration: Optional[str] = None
    version: bool = False
    debug: bool = False
    sequential: bool = False
    strict: bool = False
    show_error_traces: bool = False
    output: str = TEXT
    enable_profiling: bool = False
    enable_memory_profiling: bool = False
    noninteractive: bool = False
    logging_sections: Optional[str] = None
    log_identifier: Optional[str] = None
    logger: Optional[str] = None
    targets: List[str] = field(default_factory=list)
    source_directories: List[str] = field(default_factory=list)
    only_check_paths: List[str] = field(default_factory=list)
    buck_mode: Optional[str] = None
    no_saved_state: bool = False
    search_path: List[str] = field(default_factory=list)
    binary: Optional[str] = None
    exclude: List[str] = field(default_factory=list)
    typeshed: Optional[str] = None
    save_initial_state_to: Optional[str] = None
    load_initial_state_from: Optional[str] = None
    changed_files_path: Optional[str] = None
    saved_state_project: Optional[str] = None
    dot_pyre_directory: Optional[Path] = None
    isolation_prefix: Optional[str] = None
    python_version: Optional[str] = None
    shared_memory_heap_size: Optional[int] = None
    shared_memory_dependency_table_power: Optional[int] = None
    shared_memory_hash_table_power: Optional[int] = None
    number_of_workers: Optional[int] = None
    enable_hover: Optional[bool] = None
    enable_go_to_definition: Optional[bool] = None
    enable_find_symbols: Optional[bool] = None
    enable_find_all_references: Optional[bool] = None
    enable_expression_level_coverage: Optional[bool] = None
    enable_consume_unsaved_changes: Optional[bool] = None
    use_buck2: Optional[bool] = None


@dataclass(frozen=True)
class StartArguments:
    changed_files_path: Optional[str] = None
    debug: bool = False
    enable_memory_profiling: bool = False
    enable_profiling: bool = False
    load_initial_state_from: Optional[str] = None
    log_identifier: Optional[str] = None
    logging_sections: Optional[str] = None
    no_saved_state: bool = False
    no_watchman: bool = False
    noninteractive: bool = False
    save_initial_state_to: Optional[str] = None
    saved_state_project: Optional[str] = None
    sequential: bool = False
    show_error_traces: bool = False
    store_type_check_resolution: bool = False
    terminal: bool = False
    wait_on_initialization: bool = False
    skip_initial_type_check: bool = False
    use_lazy_module_tracking: bool = False

    @staticmethod
    def create(
        command_argument: CommandArguments,
        no_watchman: bool = False,
        store_type_check_resolution: bool = False,
        wait_on_initialization: bool = False,
        terminal: bool = False,
        skip_initial_type_check: bool = False,
        use_lazy_module_tracking: bool = False,
    ) -> StartArguments:
        return StartArguments(
            changed_files_path=command_argument.changed_files_path,
            debug=command_argument.debug,
            enable_memory_profiling=command_argument.enable_memory_profiling,
            enable_profiling=command_argument.enable_profiling,
            load_initial_state_from=command_argument.load_initial_state_from,
            log_identifier=command_argument.log_identifier,
            logging_sections=command_argument.logging_sections,
            no_saved_state=command_argument.no_saved_state,
            no_watchman=no_watchman,
            noninteractive=command_argument.noninteractive,
            save_initial_state_to=command_argument.save_initial_state_to,
            saved_state_project=command_argument.saved_state_project,
            sequential=command_argument.sequential,
            show_error_traces=command_argument.show_error_traces,
            store_type_check_resolution=store_type_check_resolution,
            terminal=terminal,
            wait_on_initialization=wait_on_initialization,
            skip_initial_type_check=skip_initial_type_check,
            use_lazy_module_tracking=use_lazy_module_tracking,
        )


@dataclass(frozen=True)
class IncrementalArguments:
    output: str = TEXT
    no_start: bool = False
    start_arguments: StartArguments = field(default_factory=StartArguments)


@dataclass(frozen=True)
class CheckArguments:
    debug: bool = False
    enable_memory_profiling: bool = False
    enable_profiling: bool = False
    log_identifier: Optional[str] = None
    logging_sections: Optional[str] = None
    noninteractive: bool = False
    output: str = TEXT
    sequential: bool = False
    show_error_traces: bool = False

    @staticmethod
    def create(
        command_argument: CommandArguments,
    ) -> CheckArguments:
        return CheckArguments(
            debug=command_argument.debug,
            enable_memory_profiling=command_argument.enable_memory_profiling,
            enable_profiling=command_argument.enable_profiling,
            log_identifier=command_argument.log_identifier,
            logging_sections=command_argument.logging_sections,
            noninteractive=command_argument.noninteractive,
            output=command_argument.output,
            sequential=command_argument.sequential,
            show_error_traces=command_argument.show_error_traces,
        )


@dataclass(frozen=True)
class InferArguments:
    working_directory: Path
    annotate_attributes: bool = False
    annotate_from_existing_stubs: bool = False
    debug_infer: bool = False
    quote_annotations: bool = False
    dequalify: bool = False
    enable_memory_profiling: bool = False
    enable_profiling: bool = False
    log_identifier: Optional[str] = None
    logging_sections: Optional[str] = None
    use_future_annotations: bool = False
    in_place: bool = False
    simple_annotations: bool = False
    paths_to_modify: Optional[Set[Path]] = None
    print_only: bool = False
    read_stdin: bool = False
    sequential: bool = False


@dataclass(frozen=True)
class RageArguments:
    output: Optional[Path] = None
    server_log_count: Optional[int] = None


@dataclass(frozen=True)
class StatisticsArguments:
    directories: List[str] = field(default_factory=list)
    log_identifier: Optional[str] = None
    log_results: bool = False
    aggregate: bool = False
    print_summary: bool = False


@dataclass(frozen=True)
class CoverageArguments:
    working_directory: str
    paths: List[str] = field(default_factory=list)
    print_summary: bool = False


@dataclass(frozen=True)
class AnalyzeArguments:
    debug: bool = False
    dump_call_graph: Optional[str] = None
    dump_model_query_results: Optional[str] = None
    enable_memory_profiling: bool = False
    enable_profiling: bool = False
    find_missing_flows: Optional[MissingFlowsKind] = None
    inline_decorators: bool = False
    log_identifier: Optional[str] = None
    maximum_tito_depth: Optional[int] = None
    maximum_trace_length: Optional[int] = None
    no_verify: bool = False
    verify_dsl: bool = False
    output: str = TEXT
    repository_root: Optional[str] = None
    rule: List[int] = field(default_factory=list)
    source: List[str] = field(default_factory=list)
    sink: List[str] = field(default_factory=list)
    transform: List[str] = field(default_factory=list)
    save_results_to: Optional[str] = None
    sequential: bool = False
    taint_models_path: List[str] = field(default_factory=list)
    use_cache: bool = False
