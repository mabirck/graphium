class Graphium::AgentController < ApplicationController
    def index
        @agents = Graphium::AgentStory.where({'active': true})
    end
end
