class Graphium::StreetController < ApplicationController
    def index
        @streets = Graphium::Street.where(:name_osm.nin => ["", nil]).limit(200)
    end
end
