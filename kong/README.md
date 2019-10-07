# Kong Integration

## Overview

The Agent's Kong check tracks total requests, response codes, client connections, and more.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][1] for guidance on applying these instructions.

### Installation

The Kong check is included in the [Datadog Agent][2] package, so you don't need to install anything else on your Kong servers.

### Configuration

Edit the `kong.d/conf.yaml` file, in the `conf.d/` folder at the root of your [Agent's configuration directory][3].

#### Metric collection

1. Add this configuration block to your `kong.d/conf.yaml` file to start gathering your [Kong Metrics](#metrics):

    ```yaml
      init_config:

      instances:
        # Each instance needs a `kong_status_url`. Tags are optional.
        - kong_status_url: http://example.com:8001/status/
          tags:
            - instance:foo
        - kong_status_url: http://example2.com:8001/status/
          tags:
            - instance:bar
    ```

    See the [sample kong.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

#### Log collection

**Available for Agent >6.0**

Kong access logs are generated by NGINX, so the default location is the same as for NGINX files.

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

    ```yaml
      logs_enabled: true
    ```

2. Add this configuration block to your `kong.d/conf.yaml` file to start collecting your Kong Logs:

    ```
      logs:
        - type: file
          path: /var/log/nginx/access.log
          service: <SERVICE>
          source: kong

        - type: file
          path: /var/log/nginx/error.log
          service: <SERVICE>
          source: kong
    ```

    Change the `path` and `service` parameter values and configure them for your environment.
    See the [sample kong.d/conf.yaml][3] for all available configuration options.

3. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][6] and look for `kong` under the Checks section.

## Data Collected
### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events
The Kong check does not include any events.

### Service Checks

**kong.can_connect**:<br>
Returns `CRITICAL` if the Agent cannot connect to Kong to collect metrics, otherwise returns `OK`.

## Troubleshooting
Need help? Contact [Datadog support][8].

## Further Reading

* [Monitor Kong with our new Datadog integration][9]


[1]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-core/blob/master/kong/datadog_checks/kong/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/kong/metadata.csv
[8]: https://docs.datadoghq.com/help
[9]: https://www.datadoghq.com/blog/monitor-kong-datadog