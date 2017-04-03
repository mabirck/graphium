class Graphium::Configuration
  include Mongoid::Document
  field :swarm_agent_number, type: Integer
  field :swarm_agent_names_API, type: String
  field :swarm_agent_names, type: Array
  field :swarm_agent_colors, type: Array
  field :mongo_db, type: String
  field :mongo_host, type: String
  field :mongo_port, type: Integer
  field :inf_positive, type: Integer
  field :inf_negative, type: Integer
  field :osmapi_user, type: String
  field :osmapi_password, type: String
    
  store_in collection: "configuration", database: "graphium"
end
