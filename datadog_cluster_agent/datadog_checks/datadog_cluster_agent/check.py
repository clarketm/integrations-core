# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base import OpenMetricsBaseCheck


class DatadogClusterAgentCheck(OpenMetricsBaseCheck):
    """
    Collect Cluster Agent metrics from its Prometheus endpoint
    """

    def __init__(self, name, init_config, instances):
        metrics = {
            'admission_webhooks_certificate_expiry': 'admission_webhooks_certificate_expiry',
            'admission_webhooks_mutation_attempts': 'admission_webhooks_mutation_attempts',
            'admission_webhooks_reconcile_success': 'admission_webhooks_reconcile_success',
            'admission_webhooks_webhooks_received': 'admission_webhooks_webhooks_received',
            'aggregator__flush': 'aggregator.flush',
            'aggregator__processed': 'aggregator.processed',
            'api_requests': 'api_requests',
            'checks__events': 'checks.events',
            'checks__execution_time': 'checks.execution_time',
            'checks__metrics_samples': 'checks.metrics_samples',
            'checks__runs': 'checks.runs',
            'checks__services_checks': 'checks.services_checks',
            'checks__warnings': 'checks.warnings',
            'cluster_checks_busyness': 'cluster_checks_busyness',
            'cluster_checks_configs_dangling': 'cluster_checks_configs_dangling',
            'cluster_checks_configs_dispatched': 'cluster_checks_configs_dispatched',
            'cluster_checks_nodes_reporting': 'cluster_checks_nodes_reporting',
            'cluster_checks_rebalancing_decisions': 'cluster_checks_rebalancing_decisions',
            'cluster_checks_rebalancing_duration_seconds': 'cluster_checks_rebalancing_duration_seconds',
            'cluster_checks_successful_rebalancing_moves': 'cluster_checks_successful_rebalancing_moves',
            'cluster_checks_updating_stats_duration_seconds': 'cluster_checks_updating_stats_duration_seconds',
            'datadog_requests': 'datadog_requests',
            'external_metrics_delay_seconds': 'external_metrics_delay_seconds',
            'external_metrics_processed_value': 'external_metrics_processed_value',
            'forwarder__connection_events': 'forwarder.connection_events',
            'forwarder__transactions': 'forwarder.transactions',
            'leader_election_is_leader': 'leader_election_is_leader',
            'rate_limit_queries_limit': 'rate_limit_queries_limit',
            'rate_limit_queries_period': 'rate_limit_queries_period',
            'rate_limit_queries_remaining': 'rate_limit_queries_remaining',
            'rate_limit_queries_reset': 'rate_limit_queries_reset',
            'scheduler__checks_entered': 'scheduler.checks_entered',
            'scheduler__queues_count': 'scheduler.queues_count',
            'transactions__retry_queue_size': 'transactions.retry_queue_size',
            'transactions__success': 'transactions.success',
        }
        default_namespace = 'datadog.cluster_agent'
        default_instances = {
            'datadog.cluster_agent': {
                'namespace': default_namespace,
                'metrics': [metrics],
                'send_monotonic_counter': False,
                # 'label_joins': {
                #     'leader_election_is_leader': {'labels_to_match': ['join_leader'], 'labels_to_get': ['is_leader']}
                # },
            },
        }

        super(DatadogClusterAgentCheck, self).__init__(
            name, init_config, instances, default_namespace=default_namespace, default_instances=default_instances
        )
