class Graphium::City
  include Mongoid::Document
  field :name, type: String
  field :state, type: String
  field :state_code, type: String
  field :country, type: String
  field :country_code, type: String
  field :population, type: Integer
  field :osm_node_id, type: Integer
  field :city_id, type: String  
  store_in collection: "city", database: "graphium"
end
