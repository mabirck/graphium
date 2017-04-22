class Graphium::Swarm
    include Mongoid::Document
    field :name, type: String
    field :identifier, type: String
    field :city_id, type: String
    field :num_agent, type: Integer
    field :user_email, type: String
    field :active, type: Boolean
    field :host, type: String
    field :logs, type: Array
    field :cycles, type: Integer
    field :start_at, type: String
    field :end_at, type: String
    field :qmi, type: Float
    field :end_well, type: Boolean
    field :seconds_to_check_agents, type: Integer
    store_in collection: "swarm", database: "graphium"
end
