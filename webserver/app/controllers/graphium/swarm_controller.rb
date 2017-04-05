class Graphium::SwarmController < ApplicationController
    
    layout "inside"
    def index
        @swarms = Graphium::Swarm.all#where({'active': true})
    end
end
