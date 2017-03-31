class Graphium::AgentStory
    include Mongoid::Document
    field :identifier, type: String
    field :name, type: String
    field :last_lng, type: Float
    field :last_lat, type: Float
    field :last_street, type: String
    field :host, type: String
    field :swarm_identifier, type: String
    field :end_at, type: String
    field :active, type: Boolean
    field :pathbread, type: Array
    field :color, type: String
    field :last_street_id_osm, type: Integer
    store_in collection: "agent_story", database: "graphium"
end