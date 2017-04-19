class Graphium::Wishlist
  include Mongoid::Document
  field :address, type: String
  field :lat, type: Float
  field :lng, type: Float
  field :dt_required, type: String
  field :user_email, type: String
  field :processed, type: Boolean
  field :swarm_identifier, type: String
  field :osm_way_id, type: Integer
  field :city_id, type: String
  field :priority, type: Float
  store_in collection: "wish_list", database: "graphium"
end
