class Graphium::StreetController < ApplicationController
    layout "inside"
    before_filter :authenticate_user!
    def index
        @streets = Graphium::Street.where(:name_osm.nin => ["", nil]).limit(200)
    end
end
