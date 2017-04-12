class Graphium::SwarmController < ApplicationController
    
    layout "inside"
    before_filter :authenticate_user!
    def index
        @swarms = Graphium::Swarm.all#where({'active': true})
    end
    
    def createSession
    end
end
