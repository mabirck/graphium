class Graphium::Swarm
    include Mongoid::Document
    field :name, type: String
    field :identifier, type: String
    field :num_agent, type: Integer
    field :user_email, type: String
    field :active, type: Boolean
    field :host, type: String
    store_in collection: "swarm", database: "graphium"
end
