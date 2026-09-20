/**
 * @name Path injection with AuthGap entry arguments as sources (fair comparison, prereg §5 #4)
 * @description Same as py/path-injection but the source set is the parameters of the tool
 *              entry functions that AuthGap recognises in this tree (docs/preregistration.md §5 #4).
 * @kind path-problem
 * @problem.severity error
 * @security-severity 7.5
 * @precision high
 * @id py/authgap-path-injection
 * @tags security
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.security.dataflow.PathInjectionCustomizations
import semmle.python.security.dataflow.PathInjectionQuery
import PathInjectionFlow::PathGraph

private predicate authgapEntry(string relpath, string name) {
  relpath = "examples/catalog/template_finder_agent.py" and name = "get_template_details_tool"
  or
  relpath = "examples/catalog/template_finder_agent.py" and name = "list_all_templates_tool"
  or
  relpath = "examples/catalog/template_finder_agent.py" and name = "search_templates_tool"
  or
  relpath = "examples/guardrail_example_fixed.py" and name = "get_url_context"
  or
  relpath = "examples/middleware/basic_middleware.py" and name = "get_weather"
  or
  relpath = "examples/middleware/injected_state.py" and name = "show_context"
  or
  relpath = "examples/performance/lite_agent_example.py" and name = "add_numbers"
  or
  relpath = "examples/performance/lite_agent_example.py" and name = "multiply_numbers"
  or
  relpath = "examples/python/agents/code-agent.py" and name = "analyze_code_complexity"
  or
  relpath = "examples/python/agents/code-agent.py" and name = "run_python_code"
  or
  relpath = "examples/python/agents/math-agent.py" and name = "basic_calculator"
  or
  relpath = "examples/python/agents/math-agent.py" and name = "calculate_statistics"
  or
  relpath = "examples/python/agents/math-agent.py" and name = "solve_quadratic"
  or
  relpath = "examples/python/concepts/reasoning-extraction.py" and name = "save_reasoning_chain"
  or
  relpath = "examples/python/custom_tools/latency_tracker_tool.py" and name = "latency_tracking_tool"
  or
  relpath = "examples/python/handoff/handoff_customer_service.py" and name = "get_faq_answer"
  or
  relpath = "examples/python/lite_agent_example.py" and name = "add_numbers"
  or
  relpath = "examples/python/mcp/custom-python-server.py" and name = "get_stock_price"
  or
  relpath = "examples/python/mcp/multiple-mcp-servers.py" and name = "my_custom_tool"
  or
  relpath = "examples/python/monitoring/08_custom_tools_monitoring.py" and name = "call_external_api"
  or
  relpath = "examples/python/monitoring/08_custom_tools_monitoring.py" and name = "file_operation"
  or
  relpath = "examples/python/monitoring/08_custom_tools_monitoring.py" and name = "process_data"
  or
  relpath = "examples/python/monitoring/08_custom_tools_monitoring.py" and name = "query_database"
  or
  relpath = "examples/python/plugin_template/src/praisonai_example_plugin/__init__.py" and name = "reverse_text"
  or
  relpath = "examples/python/stateful/01_basic_state_management.py" and name = "add_feature"
  or
  relpath = "examples/python/stateful/01_basic_state_management.py" and name = "check_budget_health"
  or
  relpath = "examples/python/stateful/01_basic_state_management.py" and name = "display_project_status"
  or
  relpath = "examples/python/stateful/01_basic_state_management.py" and name = "update_project_stage"
  or
  relpath = "examples/python/stateful/02_state_in_tool_functions.py" and name = "generate_report"
  or
  relpath = "examples/python/stateful/02_state_in_tool_functions.py" and name = "log_error"
  or
  relpath = "examples/python/stateful/02_state_in_tool_functions.py" and name = "process_data_batch"
  or
  relpath = "examples/python/stateful/02_state_in_tool_functions.py" and name = "track_progress"
  or
  relpath = "examples/python/stateful/02_state_in_tool_functions.py" and name = "update_configuration"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "check_budget_status"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "check_performance"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "continue_development"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "expand_features"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "generate_decision_report"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "maintain_current_setup"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "optimize_performance"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "reduce_costs"
  or
  relpath = "examples/python/stateful/03_conditional_task_execution.py" and name = "scale_infrastructure"
  or
  relpath = "examples/python/stateful/04_session_state_persistence.py" and name = "check_processing_status"
  or
  relpath = "examples/python/stateful/04_session_state_persistence.py" and name = "generate_session_report"
  or
  relpath = "examples/python/stateful/04_session_state_persistence.py" and name = "process_customer_data"
  or
  relpath = "examples/python/stateful/04_session_state_persistence.py" and name = "save_checkpoint"
  or
  relpath = "examples/python/stateful/04_session_state_persistence.py" and name = "simulate_long_task"
  or
  relpath = "examples/python/stateful/05_loop_control_with_state.py" and name = "collect_paginated_data"
  or
  relpath = "examples/python/stateful/05_loop_control_with_state.py" and name = "generate_loop_report"
  or
  relpath = "examples/python/stateful/05_loop_control_with_state.py" and name = "process_batch"
  or
  relpath = "examples/python/stateful/05_loop_control_with_state.py" and name = "process_retry_batch"
  or
  relpath = "examples/python/stateful/05_loop_control_with_state.py" and name = "validate_collected_items"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "aggregate_distributed_state"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "calculate_derived_metrics"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "generate_advanced_report"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "handle_state_transactions"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "implement_state_cache"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "manage_nested_state"
  or
  relpath = "examples/python/stateful/06_advanced_state_operations.py" and name = "manage_state_versioning"
  or
  relpath = "examples/python/stateful/workflow-state-example.py" and name = "analysis_tool"
  or
  relpath = "examples/python/stateful/workflow-state-example.py" and name = "research_tool"
  or
  relpath = "examples/python/tools/langchain/agentql-toolkit.py" and name = "extract_web_data_tool"
  or
  relpath = "examples/python/tools/langchain/brave-search.py" and name = "search_brave"
  or
  relpath = "examples/python/tools/langchain/exa-search.py" and name = "search_and_contents"
  or
  relpath = "examples/python/tools/langchain/jina-search.py" and name = "invoke_jina_search"
  or
  relpath = "examples/python/tools/trafilatura/trafilatura_example.py" and name = "extract_content_tool"
  or
  relpath = "examples/python/tools/trafilatura/trafilatura_example.py" and name = "extract_metadata_tool"
  or
  relpath = "examples/python/usecases/adaptive-learning.py" and name = "adapt_difficulty"
  or
  relpath = "examples/python/usecases/adaptive-learning.py" and name = "assess_student_level"
  or
  relpath = "examples/python/usecases/adaptive-learning.py" and name = "evaluate_performance"
  or
  relpath = "examples/python/usecases/adaptive-learning.py" and name = "generate_content"
  or
  relpath = "examples/python/usecases/climate-impact.py" and name = "analyze_urban_factors"
  or
  relpath = "examples/python/usecases/climate-impact.py" and name = "collect_environmental_data"
  or
  relpath = "examples/python/usecases/climate-impact.py" and name = "generate_adaptation_strategies"
  or
  relpath = "examples/python/usecases/climate-impact.py" and name = "model_microclimate"
  or
  relpath = "examples/python/usecases/climate-impact.py" and name = "predict_impacts"
  or
  relpath = "examples/python/usecases/crypto-validator.py" and name = "analyze_cryptographic_scheme"
  or
  relpath = "examples/python/usecases/crypto-validator.py" and name = "assess_implementation"
  or
  relpath = "examples/python/usecases/crypto-validator.py" and name = "simulate_quantum_attacks"
  or
  relpath = "examples/python/usecases/crypto-validator.py" and name = "validate_compliance"
  or
  relpath = "examples/python/usecases/customer-service.py" and name = "classify_query"
  or
  relpath = "examples/python/usecases/customer-service.py" and name = "evaluate_satisfaction"
  or
  relpath = "examples/python/usecases/customer-service.py" and name = "handle_query"
  or
  relpath = "examples/python/usecases/customer-service.py" and name = "optimize_response"
  or
  relpath = "examples/python/usecases/defi-market-maker.py" and name = "analyze_market_conditions"
  or
  relpath = "examples/python/usecases/defi-market-maker.py" and name = "assess_risks"
  or
  relpath = "examples/python/usecases/defi-market-maker.py" and name = "detect_arbitrage"
  or
  relpath = "examples/python/usecases/defi-market-maker.py" and name = "execute_trades"
  or
  relpath = "examples/python/usecases/defi-market-maker.py" and name = "optimize_liquidity"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "assess_emergency_level"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "assess_resources"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "check_network_status"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "execute_distribution"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "generate_distribution_plan"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "monitor_effectiveness"
  or
  relpath = "examples/python/usecases/disaster-recovery.py" and name = "prioritize_needs"
  or
  relpath = "examples/python/usecases/domain-context-solution.py" and name = "query_api_ninjas"
  or
  relpath = "examples/python/usecases/domain-context-solution.py" and name = "query_crtsh"
  or
  relpath = "examples/python/usecases/domain-context-solution.py" and name = "query_fofa"
  or
  relpath = "examples/python/usecases/domain-context-solution.py" and name = "query_networkcalc"
  or
  relpath = "examples/python/usecases/domain-context-solution.py" and name = "query_whoxy"
  or
  relpath = "examples/python/usecases/emergency-response.py" and name = "assess_emergency"
  or
  relpath = "examples/python/usecases/emergency-response.py" and name = "dispatch_resources"
  or
  relpath = "examples/python/usecases/emergency-response.py" and name = "monitor_response"
  or
  relpath = "examples/python/usecases/fraud-detection.py" and name = "analyze_transaction"
  or
  relpath = "examples/python/usecases/fraud-detection.py" and name = "check_patterns"
  or
  relpath = "examples/python/usecases/fraud-detection.py" and name = "generate_alert"
  or
  relpath = "examples/python/usecases/fraud-detection.py" and name = "verify_identity"
  or
  relpath = "examples/python/usecases/healthcare-diagnosis.py" and name = "analyze_medical_history"
  or
  relpath = "examples/python/usecases/healthcare-diagnosis.py" and name = "analyze_symptoms"
  or
  relpath = "examples/python/usecases/healthcare-diagnosis.py" and name = "generate_diagnosis"
  or
  relpath = "examples/python/usecases/healthcare-diagnosis.py" and name = "process_lab_results"
  or
  relpath = "examples/python/usecases/healthcare-diagnosis.py" and name = "recommend_treatment"
  or
  relpath = "examples/python/usecases/medicine-protocol.py" and name = "analyze_drug_interactions"
  or
  relpath = "examples/python/usecases/medicine-protocol.py" and name = "analyze_genetic_markers"
  or
  relpath = "examples/python/usecases/medicine-protocol.py" and name = "evaluate_patient_history"
  or
  relpath = "examples/python/usecases/medicine-protocol.py" and name = "generate_protocol"
  or
  relpath = "examples/python/usecases/medicine-protocol.py" and name = "simulate_effectiveness"
  or
  relpath = "examples/python/usecases/multilingual-content.py" and name = "adapt_content"
  or
  relpath = "examples/python/usecases/multilingual-content.py" and name = "check_cultural_context"
  or
  relpath = "examples/python/usecases/multilingual-content.py" and name = "generate_base_content"
  or
  relpath = "examples/python/usecases/multilingual-content.py" and name = "quality_check"
  or
  relpath = "examples/python/usecases/multilingual-content.py" and name = "translate_content"
  or
  relpath = "examples/python/usecases/neural-architecture.py" and name = "analyze_hardware_constraints"
  or
  relpath = "examples/python/usecases/neural-architecture.py" and name = "estimate_performance"
  or
  relpath = "examples/python/usecases/neural-architecture.py" and name = "generate_architecture_candidates"
  or
  relpath = "examples/python/usecases/neural-architecture.py" and name = "optimize_deployment"
  or
  relpath = "examples/python/usecases/neural-architecture.py" and name = "optimize_hyperparameters"
  or
  relpath = "examples/python/usecases/predictive-maintenance.py" and name = "analyze_performance"
  or
  relpath = "examples/python/usecases/predictive-maintenance.py" and name = "collect_sensor_data"
  or
  relpath = "examples/python/usecases/predictive-maintenance.py" and name = "detect_anomalies"
  or
  relpath = "examples/python/usecases/predictive-maintenance.py" and name = "predict_failures"
  or
  relpath = "examples/python/usecases/predictive-maintenance.py" and name = "schedule_maintenance"
  or
  relpath = "examples/python/usecases/quantum-optimiser.py" and name = "analyze_quantum_circuit"
  or
  relpath = "examples/python/usecases/quantum-optimiser.py" and name = "identify_optimization_opportunities"
  or
  relpath = "examples/python/usecases/quantum-optimiser.py" and name = "simulate_optimization"
  or
  relpath = "examples/python/usecases/quantum-optimiser.py" and name = "validate_results"
  or
  relpath = "examples/python/usecases/research-assistant.py" and name = "analyze_research_papers"
  or
  relpath = "examples/python/usecases/research-assistant.py" and name = "design_experiment"
  or
  relpath = "examples/python/usecases/research-assistant.py" and name = "identify_knowledge_gaps"
  or
  relpath = "examples/python/usecases/research-assistant.py" and name = "predict_impact"
  or
  relpath = "examples/python/usecases/research-assistant.py" and name = "validate_methodology"
  or
  relpath = "examples/python/usecases/smart-city.py" and name = "analyze_patterns"
  or
  relpath = "examples/python/usecases/smart-city.py" and name = "implement_changes"
  or
  relpath = "examples/python/usecases/smart-city.py" and name = "monitor_feedback"
  or
  relpath = "examples/python/usecases/smart-city.py" and name = "monitor_utilities"
  or
  relpath = "examples/python/usecases/smart-city.py" and name = "optimize_resources"
  or
  relpath = "examples/python/usecases/space-mission.py" and name = "analyze_mission_parameters"
  or
  relpath = "examples/python/usecases/space-mission.py" and name = "calculate_resource_requirements"
  or
  relpath = "examples/python/usecases/space-mission.py" and name = "optimize_allocation"
  or
  relpath = "examples/python/usecases/space-mission.py" and name = "plan_contingencies"
  or
  relpath = "examples/python/usecases/space-mission.py" and name = "simulate_mission_scenarios"
  or
  relpath = "examples/python/usecases/supply-chain.py" and name = "analyze_supply_impact"
  or
  relpath = "examples/python/usecases/supply-chain.py" and name = "generate_mitigation_strategies"
  or
  relpath = "examples/python/usecases/supply-chain.py" and name = "monitor_global_events"
  or
  relpath = "examples/python/usecases/vulnerability-detection.py" and name = "analyze_attack_vectors"
  or
  relpath = "examples/python/usecases/vulnerability-detection.py" and name = "generate_signatures"
  or
  relpath = "examples/python/usecases/vulnerability-detection.py" and name = "scan_code_patterns"
  or
  relpath = "examples/python/usecases/vulnerability-detection.py" and name = "simulate_exploitation"
  or
  relpath = "examples/python/usecases/vulnerability-detection.py" and name = "validate_findings"
  or
  relpath = "examples/scientific_writing/scientific_writer.py" and name = "format_citation"
  or
  relpath = "examples/scientific_writing/scientific_writer.py" and name = "format_latex_section"
  or
  relpath = "src/git/src/mcp_server_git/server.py" and name = "call_tool"
  or
  relpath = "src/praisonai-agents/08_custom_tools_monitoring.py" and name = "call_external_api"
  or
  relpath = "src/praisonai-agents/08_custom_tools_monitoring.py" and name = "file_operation"
  or
  relpath = "src/praisonai-agents/08_custom_tools_monitoring.py" and name = "process_data"
  or
  relpath = "src/praisonai-agents/08_custom_tools_monitoring.py" and name = "query_database"
  or
  relpath = "src/praisonai-agents/autoagents-tavily.py" and name = "tavily"
  or
  relpath = "src/praisonai-agents/benchmarks/real_benchmark.py" and name = "get_time"
  or
  relpath = "src/praisonai-agents/benchmarks/tools_benchmark.py" and name = "sample_tool"
  or
  relpath = "src/praisonai-agents/handoff-test.py" and name = "check_refund_policy"
  or
  relpath = "src/praisonai-agents/handoff-test.py" and name = "create_ticket"
  or
  relpath = "src/praisonai-agents/handoff-test.py" and name = "diagnose_issue"
  or
  relpath = "src/praisonai-agents/handoff-test.py" and name = "track_shipment"
  or
  relpath = "src/praisonai-agents/praisonaiagents/agent/execution_mixin.py" and name = "execute_agent_task"
  or
  relpath = "src/praisonai-agents/praisonaiagents/agent/sandbox_mixin.py" and name = "execute_python_code"
  or
  relpath = "src/praisonai-agents/praisonaiagents/agent/sandbox_mixin.py" and name = "execute_shell_command"
  or
  relpath = "src/praisonai-agents/praisonaiagents/agents/agents.py" and name = "execute_workflow_tool"
  or
  relpath = "src/praisonai-agents/praisonaiagents/mcp/mcp_server.py" and name = "tool_wrapper"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/a2ui_tools.py" and name = "send_a2ui_messages"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/ast_grep_tool.py" and name = "ast_grep_rewrite"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/ast_grep_tool.py" and name = "ast_grep_scan"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/ast_grep_tool.py" and name = "ast_grep_search"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/decorator.py" and name = "tool"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/duckduckgo_tools.py" and name = "duckduckgo"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/email_tools.py" and name = "list_emails"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/email_tools.py" and name = "read_email"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/email_tools.py" and name = "reply_email"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/email_tools.py" and name = "send_email"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/email_tools.py" and name = "smtp_read_inbox"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/email_tools.py" and name = "smtp_send_email"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/exa_tools.py" and name = "exa_search"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/github_tools.py" and name = "github_commit_and_push"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/github_tools.py" and name = "github_create_branch"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/github_tools.py" and name = "github_create_pull_request"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/learning.py" and name = "search_learning"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/learning.py" and name = "store_learning"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/memory.py" and name = "search_memory"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/python_tools.py" and name = "disassemble_code"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/python_tools.py" and name = "execute_code"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/python_tools.py" and name = "format_code"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/python_tools.py" and name = "lint_code"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/searxng_tools.py" and name = "searxng_search"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/tavily_tools.py" and name = "tavily_extract"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/web_crawl_tools.py" and name = "web_crawl"
  or
  relpath = "src/praisonai-agents/praisonaiagents/tools/youdotcom_tools.py" and name = "ydc_search"
  or
  relpath = "src/praisonai-agents/test_fix_verification.py" and name = "simple_tool"
  or
  relpath = "src/praisonai-agents/test_self_reflection_with_tools_verification.py" and name = "simple_calculator"
  or
  relpath = "src/praisonai-agents/test_user_code_pattern.py" and name = "google_web_search_llm"
  or
  relpath = "src/praisonai-agents/test_validation_feedback.py" and name = "mock_web_search"
  or
  relpath = "src/praisonai-agents/tests/crewai-tools-example.py" and name = "_run"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "advanced_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "backup_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "basic_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "network_dependent_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "recovery_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "step_one_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "step_two_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/error/test_error_recovery_live.py" and name = "unreliable_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "fallback_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "mcp_server_a_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "mcp_server_b_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "mcp_stock_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "mcp_streaming_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "mcp_weather_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/mcp/test_mcp_integration_live.py" and name = "unreliable_mcp_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/memory/test_memory_integration_live.py" and name = "calculate"
  or
  relpath = "src/praisonai-agents/tests/integration/memory/test_memory_integration_live.py" and name = "save_note"
  or
  relpath = "src/praisonai-agents/tests/integration/test_agent_decomposition_real.py" and name = "calculate_vault_code"
  or
  relpath = "src/praisonai-agents/tests/integration/test_agent_decomposition_real.py" and name = "echo_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/test_agent_decomposition_real.py" and name = "get_weather"
  or
  relpath = "src/praisonai-agents/tests/integration/test_loop_guardrails.py" and name = "another_broken_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/test_loop_guardrails.py" and name = "broken_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/test_loop_issue.py" and name = "another_broken_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/test_loop_issue.py" and name = "broken_weather_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/test_real_features.py" and name = "get_current_time"
  or
  relpath = "src/praisonai-agents/tests/integration/tools/test_tools_integration_live.py" and name = "backup_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/tools/test_tools_integration_live.py" and name = "calculate"
  or
  relpath = "src/praisonai-agents/tests/integration/tools/test_tools_integration_live.py" and name = "execute_python"
  or
  relpath = "src/praisonai-agents/tests/integration/tools/test_tools_integration_live.py" and name = "failing_tool"
  or
  relpath = "src/praisonai-agents/tests/integration/tools/test_tools_integration_live.py" and name = "web_search"
  or
  relpath = "src/praisonai-agents/tests/mcp-basic.py" and name = "stock_price_tool"
  or
  relpath = "src/praisonai-agents/tests/mcp-sse-direct-server.py" and name = "get_greeting"
  or
  relpath = "src/praisonai-agents/tests/mcp-sse-direct-server.py" and name = "get_weather"
  or
  relpath = "src/praisonai-agents/tests/repetitive-manual-agents.py" and name = "get_next_task"
  or
  relpath = "src/praisonai-agents/tests/repetitive-manual-agents.py" and name = "update_task_status"
  or
  relpath = "src/praisonai-agents/tests/smoke_core_phase_a_real.py" and name = "echo"
  or
  relpath = "src/praisonai-agents/tests/state_based_workflow_example.py" and name = "analyze_data_quality"
  or
  relpath = "src/praisonai-agents/tests/state_based_workflow_example.py" and name = "check_state_conditions"
  or
  relpath = "src/praisonai-agents/tests/state_based_workflow_example.py" and name = "clean_data_based_on_state"
  or
  relpath = "src/praisonai-agents/tests/state_based_workflow_example.py" and name = "generate_report_from_state"
  or
  relpath = "src/praisonai-agents/tests/state_based_workflow_example.py" and name = "process_batch_with_state"
  or
  relpath = "src/praisonai-agents/tests/state_management_example.py" and name = "add_feature_to_project"
  or
  relpath = "src/praisonai-agents/tests/state_management_example.py" and name = "check_project_status"
  or
  relpath = "src/praisonai-agents/tests/state_management_example.py" and name = "implement_next_feature"
  or
  relpath = "src/praisonai-agents/tests/state_management_example.py" and name = "initialize_project_state"
  or
  relpath = "src/praisonai-agents/tests/state_management_example.py" and name = "retrieve_session_history"
  or
  relpath = "src/praisonai-agents/tests/state_with_memory_example.py" and name = "add_conversation_turn"
  or
  relpath = "src/praisonai-agents/tests/state_with_memory_example.py" and name = "analyze_conversation_patterns"
  or
  relpath = "src/praisonai-agents/tests/state_with_memory_example.py" and name = "initialize_conversation_state"
  or
  relpath = "src/praisonai-agents/tests/state_with_memory_example.py" and name = "retrieve_user_history"
  or
  relpath = "src/praisonai-agents/tests/state_with_memory_example.py" and name = "search_conversation_memory"
  or
  relpath = "src/praisonai-agents/tests/state_with_memory_example.py" and name = "summarize_and_save_state"
  or
  relpath = "src/praisonai-agents/tests/test_architectural_fixes.py" and name = "get_news"
  or
  relpath = "src/praisonai-agents/tests/test_architectural_fixes.py" and name = "get_time"
  or
  relpath = "src/praisonai-agents/tests/test_architectural_fixes.py" and name = "get_weather"
  or
  relpath = "src/praisonai-agents/tests/test_architectural_fixes.py" and name = "slow_tool"
  or
  relpath = "src/praisonai-agents/tests/test_multiple_mcp_tools.py" and name = "get_current_time"
  or
  relpath = "src/praisonai-agents/tests/test_multiple_mcp_tools.py" and name = "mock_mcp_filesystem"
  or
  relpath = "src/praisonai-agents/tests/test_multiple_mcp_tools.py" and name = "mock_mcp_with_tools"
  or
  relpath = "src/praisonai-agents/tests/test_multiple_mcp_tools.py" and name = "sample_function"
  or
  relpath = "src/praisonai-agents/tests/test_multiple_mcp_tools.py" and name = "time_mcp"
  or
  relpath = "src/praisonai-agents/tests/test_parallel_tools.py" and name = "fetch_analytics_data"
  or
  relpath = "src/praisonai-agents/tests/test_parallel_tools.py" and name = "fetch_config_data"
  or
  relpath = "src/praisonai-agents/tests/test_parallel_tools.py" and name = "fetch_user_data"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "calculate"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "greet"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "multiply"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "my_func"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "my_search"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "search"
  or
  relpath = "src/praisonai-agents/tests/test_plugin_system.py" and name = "subtract"
  or
  relpath = "src/praisonai-agents/tests/test_self_reflection_comprehensive.py" and name = "duckduckgo_search"
  or
  relpath = "src/praisonai-agents/tests/test_tool_schema_parity.py" and name = "echo_tool"
  or
  relpath = "src/praisonai-agents/tests/test_tool_schema_parity.py" and name = "test_function"
  or
  relpath = "src/praisonai-agents/tests/test_tool_schema_parity.py" and name = "tool_one"
  or
  relpath = "src/praisonai-agents/tests/test_tool_schema_parity.py" and name = "tool_two"
  or
  relpath = "src/praisonai-agents/tests/unit/agent/test_agent_trace.py" and name = "test_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/context/test_cache_optimization.py" and name = "apple_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/context/test_cache_optimization.py" and name = "middle_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/context/test_cache_optimization.py" and name = "zebra_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_circuit_breaker.py" and name = "protected_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_injected_state.py" and name = "async_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_injected_state.py" and name = "legacy_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_injected_state.py" and name = "my_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_injected_state.py" and name = "show_state"
  or
  relpath = "src/praisonai-agents/tests/unit/test_injected_state.py" and name = "simple_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_protocols.py" and name = "my_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_decorator_retry.py" and name = "special_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_decorator_retry.py" and name = "test_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_decorator_retry.py" and name = "tool_a"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_decorator_retry.py" and name = "tool_b"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_decorator_retry.py" and name = "tool_c"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_agentic.py" and name = "async_weather_api"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_agentic.py" and name = "fallback_api"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_agentic.py" and name = "flaky_web_search"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_agentic.py" and name = "primary_api"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_agentic.py" and name = "restricted_database_query"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_integration.py" and name = "failing_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_integration.py" and name = "flaky_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_integration.py" and name = "permission_denied_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/test_tool_retry_integration.py" and name = "test_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/tools/test_availability_gating.py" and name = "available_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/tools/test_availability_gating.py" and name = "default_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/tools/test_availability_gating.py" and name = "env_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/tools/test_availability_gating.py" and name = "failing_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/tools/test_availability_gating.py" and name = "test_tool"
  or
  relpath = "src/praisonai-agents/tests/unit/tools/test_availability_gating.py" and name = "unavailable_tool"
  or
  relpath = "src/praisonai-agents/tests/workflow-test-agents.py" and name = "print_data"
  or
  relpath = "src/praisonai-agents/tests/workflow-test-agents.py" and name = "upload_to_huggingface"
  or
  relpath = "src/praisonai-agents/weather_server.py" and name = "get_weather"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "acp_create_file"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "acp_delete_file"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "acp_edit_file"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "acp_execute_command"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "list_files"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "lsp_find_definition"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "lsp_find_references"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "lsp_get_diagnostics"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "lsp_list_symbols"
  or
  relpath = "src/praisonai/praisonai/cli/features/agent_tools.py" and name = "read_file"
  or
  relpath = "src/praisonai/praisonai/code/tools/execute_command.py" and name = "execute_command"
  or
  relpath = "src/praisonai/praisonai/code/tools/write_file.py" and name = "write_file"
  or
  relpath = "src/praisonai/praisonai/context/history_store.py" and name = "history_get"
  or
  relpath = "src/praisonai/praisonai/context/history_store.py" and name = "history_search"
  or
  relpath = "src/praisonai/praisonai/context/history_store.py" and name = "history_tail"
  or
  relpath = "src/praisonai/praisonai/context/queue.py" and name = "artifact_chunk"
  or
  relpath = "src/praisonai/praisonai/context/queue.py" and name = "artifact_grep"
  or
  relpath = "src/praisonai/praisonai/context/queue.py" and name = "artifact_head"
  or
  relpath = "src/praisonai/praisonai/context/queue.py" and name = "artifact_list"
  or
  relpath = "src/praisonai/praisonai/context/queue.py" and name = "artifact_tail"
  or
  relpath = "src/praisonai/praisonai/context/terminal_logger.py" and name = "terminal_commands"
  or
  relpath = "src/praisonai/praisonai/context/terminal_logger.py" and name = "terminal_grep"
  or
  relpath = "src/praisonai/praisonai/context/terminal_logger.py" and name = "terminal_tail"
  or
  relpath = "src/praisonai/praisonai/mcp_server/tool_index.py" and name = "mcp_describe_tool"
  or
  relpath = "src/praisonai/praisonai/mcp_server/tool_index.py" and name = "mcp_list_tools"
  or
  relpath = "src/praisonai/praisonai/mcp_server/tool_index.py" and name = "mcp_search_tools"
  or
  relpath = "src/praisonai/praisonai/tools/audio.py" and name = "stt"
  or
  relpath = "src/praisonai/praisonai/tools/audio.py" and name = "tts"
  or
  relpath = "src/praisonai/praisonai/tools/skill_manage.py" and name = "skill_manage"
  or
  relpath = "src/praisonai/tests/integration/smoke_w1_robust.py" and name = "whoami"
  or
  relpath = "src/praisonai/tests/integration/test_self_improving_loop.py" and name = "isolated_skill_manage"
  or
  relpath = "src/praisonai/tests/source/autogen_langchain_tools.py" and name = "_run"
  or
  relpath = "src/praisonai/tests/source/crewai_tools.py" and name = "internet_search_tool"
  or
  relpath = "src/praisonai/tests/tools/internet_search.py" and name = "internet_search_tool"
  or
  relpath = "src/praisonai/tests/unit/gateway/test_gateway_approval_agentic.py" and name = "dangerous_tool"
  or
  relpath = "src/praisonai/tests/unit/test_ollama_fix.py" and name = "dummy_tool"
  or
  relpath = "src/praisonai/tests/yaml_example.py" and name = "_run"
}

/** A parameter of a function AuthGap treats as a tool entry. */
class AuthGapEntrySource extends PathInjection::Source {
  AuthGapEntrySource() {
    exists(Function f, Parameter p |
      authgapEntry(f.getLocation().getFile().getRelativePath(), f.getName()) and
      p = f.getAnArg() and
      this.(DataFlow::ParameterNode).getParameter() = p
    )
  }
}

from PathInjectionFlow::PathNode source, PathInjectionFlow::PathNode sink
where PathInjectionFlow::flowPath(source, sink)
select sink.getNode(), source, sink, "This path depends on a $@.", source.getNode(),
  "AuthGap entry argument"
