require 'test_helper'

class Graphium::ConfigurationsControllerTest < ActionController::TestCase
  setup do
    @graphium_configuration = graphium_configurations(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:graphium_configurations)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create graphium_configuration" do
    assert_difference('Graphium::Configuration.count') do
      post :create, graphium_configuration: { colors: @graphium_configuration.colors, inf_negative: @graphium_configuration.inf_negative, inf_positive: @graphium_configuration.inf_positive, mongo_db: @graphium_configuration.mongo_db, mongo_host: @graphium_configuration.mongo_host, mongo_port: @graphium_configuration.mongo_port, osmapi_password: @graphium_configuration.osmapi_password, osmapi_user: @graphium_configuration.osmapi_user, swarm_agent_names: @graphium_configuration.swarm_agent_names, swarm_agent_names_API: @graphium_configuration.swarm_agent_names_API, swarm_agent_number: @graphium_configuration.swarm_agent_number }
    end

    assert_redirected_to graphium_configuration_path(assigns(:graphium_configuration))
  end

  test "should show graphium_configuration" do
    get :show, id: @graphium_configuration
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @graphium_configuration
    assert_response :success
  end

  test "should update graphium_configuration" do
    patch :update, id: @graphium_configuration, graphium_configuration: { colors: @graphium_configuration.colors, inf_negative: @graphium_configuration.inf_negative, inf_positive: @graphium_configuration.inf_positive, mongo_db: @graphium_configuration.mongo_db, mongo_host: @graphium_configuration.mongo_host, mongo_port: @graphium_configuration.mongo_port, osmapi_password: @graphium_configuration.osmapi_password, osmapi_user: @graphium_configuration.osmapi_user, swarm_agent_names: @graphium_configuration.swarm_agent_names, swarm_agent_names_API: @graphium_configuration.swarm_agent_names_API, swarm_agent_number: @graphium_configuration.swarm_agent_number }
    assert_redirected_to graphium_configuration_path(assigns(:graphium_configuration))
  end

  test "should destroy graphium_configuration" do
    assert_difference('Graphium::Configuration.count', -1) do
      delete :destroy, id: @graphium_configuration
    end

    assert_redirected_to graphium_configurations_path
  end
end
