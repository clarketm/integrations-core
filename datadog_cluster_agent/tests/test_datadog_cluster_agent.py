# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.datadog_cluster_agent import DatadogClusterAgentCheck
from datadog_checks.dev.utils import get_metadata_metrics

NAMESPACE = 'datadog.cluster_agent'
METRICS = [
    NAMESPACE + '.admission_webhooks_certificate_expiry',
    NAMESPACE + '.admission_webhooks_mutation_attempts',
    NAMESPACE + '.admission_webhooks_reconcile_success',
    NAMESPACE + '.admission_webhooks_webhooks_received',
    NAMESPACE + '.aggregator.flush',
    NAMESPACE + '.aggregator.processed',
    NAMESPACE + '.api_requests',
    NAMESPACE + '.checks.events',
    NAMESPACE + '.checks.execution_time',
    NAMESPACE + '.checks.metrics_samples',
    NAMESPACE + '.checks.runs',
    NAMESPACE + '.checks.services_checks',
    NAMESPACE + '.checks.warnings',
    NAMESPACE + '.cluster_checks_busyness',
    NAMESPACE + '.cluster_checks_configs_dangling',
    NAMESPACE + '.cluster_checks_configs_dispatched',
    NAMESPACE + '.cluster_checks_nodes_reporting',
    NAMESPACE + '.cluster_checks_rebalancing_decisions',
    NAMESPACE + '.cluster_checks_rebalancing_duration_seconds',
    NAMESPACE + '.cluster_checks_successful_rebalancing_moves',
    NAMESPACE + '.cluster_checks_updating_stats_duration_seconds',
    NAMESPACE + '.datadog_requests',
    NAMESPACE + '.external_metrics_delay_seconds',
    NAMESPACE + '.external_metrics_processed_value',
    NAMESPACE + '.forwarder.connection_events',
    NAMESPACE + '.forwarder.transactions',
    NAMESPACE + '.leader_election_is_leader',
    NAMESPACE + '.rate_limit_queries_limit',
    NAMESPACE + '.rate_limit_queries_period',
    NAMESPACE + '.rate_limit_queries_remaining',
    NAMESPACE + '.rate_limit_queries_reset',
    NAMESPACE + '.scheduler.checks_entered',
    NAMESPACE + '.scheduler.queues_count',
    NAMESPACE + '.transactions.retry_queue_size',
    NAMESPACE + '.transactions.success',
]


def test_check(aggregator, instance, mock_get):
    check = DatadogClusterAgentCheck('datadog_cluster_agent', {}, [instance])
    check.check(instance)

    for metric in METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
