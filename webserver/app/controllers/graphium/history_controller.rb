class Graphium::HistoryController < ApplicationController
    layout "inside"
    def index
        @agents = Graphium::AgentStory.all
    end
end
