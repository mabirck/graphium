class Graphium::Street
    include Mongoid::Document
    field :name_osm, type: String
    field :type_osm, type: String
    field :surface_osm, type: String
    field :nodes, type: Array
    field :id_osm, type: Integer
    store_in collection: "street", database: "graphium"
end
