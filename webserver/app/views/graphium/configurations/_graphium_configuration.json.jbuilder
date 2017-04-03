json.extract! graphium_configuration, :id, :swarm_agent_number, :swarm_agent_names_API, :swarm_agent_names, :mongo_db, :mongo_host, :mongo_port, :colors, :inf_positive, :inf_negative, :osmapi_user, :osmapi_password, :created_at, :updated_at
json.url graphium_configuration_url(graphium_configuration, format: :json)
