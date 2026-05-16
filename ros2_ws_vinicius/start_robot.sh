#Define o caminho do workspace (Aqui vices podem alterar com a pasta de voces)
WORKSPACE_DIR=~/ros2_ws_vinicius

echo = "===Iniciando Sistema do Robô==="
echo "WorkSpace: $WORKSPACE_DIR"

#Entrada na pasta
cd $WORKSPACE_DIR

if [ ! -f "install/setup.bash" ]; then
     
	echo"ERRO: arquivo install/setup.bash não encontrado, Compila ele"
	exit 1
fi

#Abre o terminal com os 4 rodando
gnome-terminal --window \
--tab --title="1-Gazebo" --command="bash -c 'source /opt/ros/humble/setup.bash; source install/setup.bash; ros2 launch robot_bringup gazebo_world.launch.py; exec bash'" \
  --tab --title="2-SLAM/Map" --command="bash -c 'sleep 5; source /opt/ros/humble/setup.bash; source install/setup.bash; ros2 launch robot_bringup mapping.launch.py; exec bash'" \
  --tab --title="3-Nav2" --command="bash -c 'sleep 8; source /opt/ros/humble/setup.bash; source install/setup.bash; ros2 launch robot_bringup navigation_launch.py; exec bash'" \
  --tab --title="4-Teleop" --command="bash -c 'sleep 10; source /opt/ros/humble/setup.bash; source install/setup.bash; ros2 launch robot_bringup teleop_keyboard.launch.py; exec bash'"

echo "Sistema Iniciado! As abas abrirão em instantes"  
