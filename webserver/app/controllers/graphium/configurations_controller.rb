class Graphium::ConfigurationsController < ApplicationController

  layout "inside"
  before_filter :authenticate_user!
  before_action :set_graphium_configuration, only: [:show, :edit, :update, :destroy]

  # GET /graphium/configurations
  # GET /graphium/configurations.json
  def index
    @graphium_configurations = Graphium::Configuration.all
  end

  # GET /graphium/configurations/1
  # GET /graphium/configurations/1.json
  def show
  end

  # GET /graphium/configurations/new
  def new
    @graphium_configuration = Graphium::Configuration.new
  end

  # GET /graphium/configurations/1/edit
  def edit
  end

  # POST /graphium/configurations
  # POST /graphium/configurations.json
  def create
    @graphium_configuration = Graphium::Configuration.new(graphium_configuration_params)

    respond_to do |format|
      if @graphium_configuration.save
        format.html { redirect_to @graphium_configuration, notice: 'Configuration was successfully created.' }
        format.json { render :show, status: :created, location: @graphium_configuration }
      else
        format.html { render :new }
        format.json { render json: @graphium_configuration.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /graphium/configurations/1
  # PATCH/PUT /graphium/configurations/1.json
  def update
    respond_to do |format|
     
      # change format of names
      names = graphium_configuration_params[:swarm_agent_names]
      names_to_save = []
      names = names.split(',')
      names.each do |name|
          names_to_save << name
      end
      graphium_configuration_params[:swarm_agent_names] = names_to_save
      
      # change format of colors
      colors = graphium_configuration_params[:swarm_agent_colors]
      colors_to_save = []
      colors = colors.split(',')
      colors.each do |color|
          colors_to_save << color
      end
      graphium_configuration_params[:swarm_agent_colors] = colors_to_save
      logger.info 'PARAMS'
      logger.info graphium_configuration_params
        
      # updating manually
      @graphium_configuration.swarm_agent_number = graphium_configuration_params[:swarm_agent_number]
      @graphium_configuration.swarm_agent_names_API = graphium_configuration_params[:swarm_agent_names_API]
      @graphium_configuration.swarm_agent_names = names_to_save
      @graphium_configuration.mongo_db = graphium_configuration_params[:mongo_db]
      @graphium_configuration.mongo_host = graphium_configuration_params[:mongo_host]
      @graphium_configuration.mongo_port = graphium_configuration_params[:mongo_port]
      @graphium_configuration.swarm_agent_colors = colors_to_save
      @graphium_configuration.inf_positive = graphium_configuration_params[:inf_positive]
      @graphium_configuration.inf_negative = graphium_configuration_params[:inf_negative]
      @graphium_configuration.osmapi_user = graphium_configuration_params[:osmapi_user]
      @graphium_configuration.osmapi_password = graphium_configuration_params[:osmapi_password]
      @graphium_configuration.swarm_seconds_to_check_agents = graphium_configuration_params[:swarm_seconds_to_check_agents]
        
      if @graphium_configuration.save
        
        format.html { redirect_to "/graphium/configurations/1/edit", notice: 'Configuration was successfully updated.' }
        format.json { render :show, status: :ok, location: @graphium_configuration }
      else
        format.html { render :edit }
        format.json { render json: @graphium_configuration.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /graphium/configurations/1
  # DELETE /graphium/configurations/1.json
  def destroy
    @graphium_configuration.destroy
    respond_to do |format|
      format.html { redirect_to graphium_configurations_url, notice: 'Configuration was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_graphium_configuration
        
      if Graphium::Configuration.all.length == 0
          Graphium::Configuration.create( :swarm_agent_number => 3, :swarm_agent_names_API => "http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all", :swarm_agent_names =>['Coralina Malaya','Abigail Johnson','Antonietta Marinese','Elisa Rogoff','Serafim Folkerts','Dulce Barrell'], :mongo_db => "graphium",:mongo_host =>"localhost",:mongo_port =>27017, :swarm_agent_colors => ["#E91E63", "#9C27B0", "#F44336", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#CDDC39", "#FF9800","#795548","#FF5722","#607D8B","#9E9E9E","#827717"],:inf_positive => 99999, :inf_negative => -99999, :osmapi_user => "glaucomunsberg",:osmapi_password =>"30271255",:swarm_seconds_to_check_agents => 3)
      end
      params[:id] = Graphium::Configuration.all.first.id
      @graphium_configuration = Graphium::Configuration.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def graphium_configuration_params
      params.require(:graphium_configuration).permit(:swarm_agent_number, :swarm_seconds_to_check_agents, :swarm_agent_names_API, :swarm_agent_names, :mongo_db, :mongo_host, :mongo_port, :swarm_agent_colors, :inf_positive, :inf_negative, :osmapi_user, :osmapi_password)
    end
end
