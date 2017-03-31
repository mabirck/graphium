class Graphium::HistoryController < ApplicationController
    def index
        @agents = Graphium::AgentStory.all
    end
end
