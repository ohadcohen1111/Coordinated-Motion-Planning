from BFS import bfs, is_valid
from MoveRobot import move_robot, move_robots_back, move_robot_to_final_place
from Point import Point
from RobotDetails import find_robot_by_number
from RobotPoint import RobotPoint


def get_direction_frame(p, n, row_space):
    if p.x <= row_space <= p.y <= n - row_space:
        return "UP"

    if n - row_space >= p.x >= row_space > p.y:
        return "LEFT"

    if p.x >= n - row_space >= p.y >= row_space:
        return "DOWN"

    if row_space <= p.x <= n - row_space <= p.y:
        return "RIGHT"


def get_robot_out(eb, robot):
    p = robot.current_place
    direction = get_direction_frame(p, eb.n, eb.row_space)
    if direction == "UP":
        move_robots_up(eb, robot)
    if direction == "RIGHT":
        move_robots_right(eb, robot)
    if direction == "DOWN":
        move_robots_down(eb, robot)
    if direction == "LEFT":
        move_robots_left(eb, robot)


def move_robots_up(eb, robot):
    number_of_steps = 0
    robot_prev_place = []
    p = robot.current_place
    x = p.x
    lines_space = eb.row_space - x - 1
    counter = 0
    while lines_space > 0:
        counter += 1
        lines_space -= 1
        x += 1

    number_steps_out = counter
    if p.y < eb.n / 2:
        while counter > 0:
            # returns the robot
            r = find_robot_by_number(eb.board[p.x + counter][p.y])
            # validity test
            if r.robot_number == 0:
                counter -= 1
                continue
            # create a point to which the robot will move
            point_temp = Point(p.x + number_steps_out + 1, p.y + counter)
            # return the route to this point
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            # If there is no path to the point, find a new point, as long as there is no correct path find a new point
            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x + number_steps_out + plus_steps, p.y + counter)
                if is_valid(p.x + number_steps_out + plus_steps, p.y + counter, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break
            # if there is a way, move the robot to the new point
            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list that will later return to the point from which it came
                robot_point = RobotPoint(r, dest)
                robot_prev_place.append(robot_point)
                # move robot to new place
                number_of_steps += move_robot(eb, r, robot_queue_node)
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        move_robot_to_final_place(eb, robot, "UP")

        # reverse the robots -> return robots
        move_robots_back(eb, robot_prev_place)

    if p.y >= eb.n / 2:
        while counter > 0:
            r = find_robot_by_number(eb.board[p.x + counter][p.y])
            if r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x + number_steps_out + 1, p.y - counter)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x + number_steps_out + plus_steps, p.y - counter)
                if is_valid(p.x + number_steps_out + plus_steps, p.y - counter, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break
            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_prev_place.append(robot_point)
                # move robot to new place
                number_of_steps += move_robot(eb, r, robot_queue_node)
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "UP")
        number_of_steps += num

        # reverse the robots -> return robots
        number_of_steps += move_robots_back(eb, robot_prev_place)

    return number_of_steps


def move_robots_down(eb, robot):
    number_of_steps = 0
    robot_old_place = []
    p = robot.current_place
    x = p.x

    lines_space = eb.row_space - (eb.n - x)
    counter = 0
    while lines_space > 0:
        counter += 1
        lines_space -= 1
        x += 1
    number_steps_out = counter
    if p.y < eb.n / 2:
        while counter > 0:
            r = find_robot_by_number(eb.board[p.x - counter][p.y])
            if r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x - number_steps_out - 1, p.y + counter)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x - number_steps_out - counter - plus_steps, p.y + counter)
                if is_valid(p.x - number_steps_out - counter - plus_steps, p.y + counter, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break

            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_old_place.append(robot_point)
                # move robot to new place
                num = move_robot(eb, r, robot_queue_node)
                number_of_steps += num
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "DOWN")
        number_of_steps += num

        # reverse the robots -> return robots
        num = move_robots_back(eb, robot_old_place)
        number_of_steps += num

    if p.y >= eb.n / 2:
        while counter > 0:
            r = find_robot_by_number(eb.board[p.x - counter][p.y])
            if r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x - number_steps_out - 1, p.y - counter)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x - number_steps_out - plus_steps, p.y - counter)
                if is_valid(p.x - number_steps_out - plus_steps, p.y - counter, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break

            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_old_place.append(robot_point)
                # move robot to new place
                num = move_robot(eb, r, robot_queue_node)
                number_of_steps += num
                counter -= 1

            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "DOWN")
        number_of_steps += num

        # reverse the robots -> return robots
        num = move_robots_back(eb, robot_old_place)
        number_of_steps += num


def move_robots_left(eb, robot):
    number_of_steps = 0
    robot_old_place = []
    p = robot.current_place
    y = p.y

    lines_space = eb.row_space - y - 1
    counter = 0

    while lines_space > 0:
        counter += 1
        lines_space -= 1
        y += 1

    number_steps_out = counter
    if p.x < eb.n / 2:
        while counter > 0:
            r = find_robot_by_number(eb.board[p.x][p.y + counter])
            if r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x + counter, p.y + number_steps_out + 1)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)
            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x + counter, p.y + number_steps_out + plus_steps)
                if is_valid(p.x + counter, p.y + number_steps_out + plus_steps, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break

            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_old_place.append(robot_point)
                # move robot to new place
                num = move_robot(eb, r, robot_queue_node)
                number_of_steps += num
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "LEFT")
        number_of_steps += num

        # reverse the robots -> return robots
        num = move_robots_back(eb, robot_old_place)
        number_of_steps += num

    if p.x >= eb.n / 2:
        while counter > 0:
            r = find_robot_by_number(eb.board[p.x][p.y + counter])
            if r == -1 or r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x - counter, p.y + number_steps_out + 1)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x - counter, p.y + number_steps_out + plus_steps)
                if is_valid(p.x - counter, p.y + number_steps_out + plus_steps, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break

            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_old_place.append(robot_point)
                # move robot to new place
                num = move_robot(eb, r, robot_queue_node)
                number_of_steps += num
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "LEFT")
        number_of_steps += num

        # reverse the robots -> return robots
        num = move_robots_back(eb, robot_old_place)
        number_of_steps += num


def move_robots_right(eb, robot):
    number_of_steps = 0
    robot_old_place = []
    p = robot.current_place
    y = p.y
    lines_space = eb.row_space - (eb.n - y)
    counter = 0

    while lines_space > 0:
        counter += 1
        lines_space -= 1
        y += 1
    number_steps_out = counter
    if p.x < eb.n / 2:
        while lines_space > 0:
            r = find_robot_by_number(eb.board[p.x][p.y - counter])
            if r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x + counter, p.y - number_steps_out - 1)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x + counter, p.y - number_steps_out - plus_steps)
                if is_valid(p.x + counter, p.y - number_steps_out - plus_steps, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break

            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_old_place.append(robot_point)
                # move robot to new place
                num = move_robot(eb, r, robot_queue_node)
                number_of_steps += num
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "RIGHT")
        number_of_steps += num

        # reverse the robots -> return robots
        num = move_robots_back(eb, robot_old_place)
        number_of_steps += num

    if p.y >= eb.n / 2:
        while counter > 0:
            r = find_robot_by_number(eb.board[p.x][p.y - counter])
            if r == -1 or r.robot_number == 0:
                counter -= 1
                continue
            point_temp = Point(p.x - counter, p.y - number_steps_out - 1)
            robot_queue_node = bfs(eb.board, r.current_place, point_temp)

            plus_steps = 1
            while robot_queue_node == -1:
                point_temp = Point(p.x - counter, p.y - number_steps_out - plus_steps)

                if is_valid(p.x - counter, p.y - number_steps_out - plus_steps, eb.n, eb.n):
                    robot_queue_node = bfs(eb.board, r.current_place, point_temp)
                    plus_steps += 1
                else:
                    break
            if robot_queue_node != -1:
                dest = Point(r.current_place.x, r.current_place.y)
                # add to back list
                robot_point = RobotPoint(r, dest)
                robot_old_place.append(robot_point)
                # move robot to new place
                num = move_robot(eb, r, robot_queue_node)
                number_of_steps += num
                counter -= 1
            else:
                counter -= 1

        # move robot to final place
        num = move_robot_to_final_place(eb, robot, "RIGHT")
        number_of_steps += num

        # reverse the robots -> return robots
        num = move_robots_back(eb, robot_old_place)
        number_of_steps += num
