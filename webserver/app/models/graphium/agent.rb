class Graphium::Agent
    include Mongoid::Document
    store_in collection: "agents", database: "graphium"
end
