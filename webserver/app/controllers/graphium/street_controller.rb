class Graphium::StreetController < ApplicationController
    layout "inside"
    def index
        @streets = Graphium::Street.where(:name_osm.nin => ["", nil]).limit(200)
    end
end
