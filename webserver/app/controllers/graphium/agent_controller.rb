class Graphium::AgentController < ApplicationController
    
    layout "inside"
    
    def index
        @agents = Graphium::Agent.all#where({'active': true})
    end
end
