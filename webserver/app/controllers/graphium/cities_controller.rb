class Graphium::CitiesController < ApplicationController
  before_action :set_graphium_city, only: [:show, :edit, :update, :destroy]
  before_filter :authenticate_user!
  layout "inside"
  # GET /graphium/cities
  # GET /graphium/cities.json
  def index
    @graphium_cities = Graphium::City.all
  end

  # GET /graphium/cities/1
  # GET /graphium/cities/1.json
  def show
  end

  # GET /graphium/cities/new
  def new
    @graphium_city = Graphium::City.new
  end

  # GET /graphium/cities/1/edit
  def edit
  end

  # POST /graphium/cities
  # POST /graphium/cities.json
  def create
    @graphium_city = Graphium::City.new(graphium_city_params)

    respond_to do |format|
      if @graphium_city.save
        format.html { redirect_to @graphium_city, notice: 'City was successfully created.' }
        format.json { render :show, status: :created, location: @graphium_city }
      else
        format.html { render :new }
        format.json { render json: @graphium_city.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /graphium/cities/1
  # PATCH/PUT /graphium/cities/1.json
  def update
    respond_to do |format|
      if @graphium_city.update(graphium_city_params)
        format.html { redirect_to @graphium_city, notice: 'City was successfully updated.' }
        format.json { render :show, status: :ok, location: @graphium_city }
      else
        format.html { render :edit }
        format.json { render json: @graphium_city.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /graphium/cities/1
  # DELETE /graphium/cities/1.json
  def destroy
    @graphium_city.destroy
    respond_to do |format|
      format.html { redirect_to graphium_cities_url, notice: 'City was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_graphium_city
      @graphium_city = Graphium::City.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def graphium_city_params
      params.require(:graphium_city).permit(:name, :state, :state_code, :country, :country_code, :population, :osm_node_id)
    end
end
