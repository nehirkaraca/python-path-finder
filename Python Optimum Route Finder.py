
# row_min_cost finds the minimum cost starting from a point (a,b).

def row_min_cost(a, b, last, total_cost, min_cost, call_c, costs, matrix):
    cost1, cost2, cost3 = tuple(costs)

    call_c += 1
    # call_c keeps track of the depth of the recursion.
    # I defined this variable because the base case for the first call of the function is different from the rest.
    # It also helped me keep track of the calculations while testing.

    if matrix[a][b] == 0:  # Checking if the step is a sinkhole
        raise ValueError
    path_list = []
    cost = 0
    check_list1 = []
    check_list2 = []

    # The following code is for determining the 0 values around the chosen box and
    # calculating the cost:

    try:
        # This part is for calculating the values of the boxes diagonal to the current box:
        if a - 1 >= 0 and b - 1 >= 0:
            c = matrix[a - 1][b - 1] # c is defined as the box one left and one up from the current box.
            check_list2.append(c)
        if a - 1 >= 0 and len(matrix[0]) > b + 1 >= 0:
            d = matrix[a - 1][b + 1]
            check_list2.append(d)
        if len(matrix) > a + 1 >= 0 and len(matrix[0]) > b + 1 >= 0:
            e = matrix[a + 1][b + 1]
            check_list2.append(e)
        if len(matrix) > a + 1 >= 0 and b - 1 >= 0:
            f = matrix[a + 1][b - 1]
            check_list2.append(f)
    except IndexError:
        pass
    try:
        # This part is for calculating the values of the boxes horizontal/vertical to the current box:
        if a >= 0 and b - 1 >= 0:
            g = matrix[a][b - 1]
            check_list1.append(g)
        if a >= 0 and len(matrix[0]) > b + 1 >= 0:
            h = matrix[a][b + 1]
            check_list1.append(h)
        if a - 1 >= 0 and b >= 0:
            i = matrix[a - 1][b]
            check_list1.append(i)
        if len(matrix) > a + 1 >= 0 and b >= 0:
            j = matrix[a + 1][b]
            check_list1.append(j)
    except IndexError:
        pass

    for i in check_list1: # If there is a 0 value in the boxes horizontal/vertical to the current box, cost is cost3.
        if i == 0:
            cost = cost3

    if cost != cost3: # No 0 in horizontal/vertical boxes, but a 0 in diagonal boxes: cost = cost2
        for i in check_list2:
            if i == 0:
                cost = cost2

    if cost != cost2 and cost != cost3: # if there are no 0 values around the box the cost is cost1.
        cost = cost1
    total_cost += cost

    if min_cost <= total_cost: # Stops after the calculated cost exceeds the minimum cost calculated so far.
        return cost + 1, path_list, min_cost
    # It doesn't matter what this part returns as long as it is bigger than the minimum so I choose (cost + 1)

    if b == len(matrix[0]) - 1 and total_cost < min_cost:
        min_cost = total_cost
    # If we have reached the end of the row, and we calculated a smaller value than the minimum cost,
    # the new minimum cost will be updated.

    if b == len(matrix[0]) - 1:  # This is the base case for the function.
        path_list.append((a, b)) # (a,b) is the coordinate of the box that is stepped on.
        return cost, path_list, min_cost
    else:
        checking = []
        try:
            if b + 1 < len(matrix[0]) and last != "l" : # Go right
                #                         ^^^^^^^^^^^^
                # We will only go right if the previous move wasn't "Go Left"
                # Otherwise the code would be stuck in a loop
                rcost, rpath, min_cost = row_min_cost(a, b + 1, "r", total_cost, min_cost, call_c, costs, matrix)
                rcost = rcost + cost # The cost from the right side (the total cost will pile up after each recursion)
                rpath.append((a, b))
                if call_c != 1:
                    checking.append(rcost)
        except ValueError:
            pass
        try:
            if last != "d" and a - 1 >= 0:  # Go up
                ucost, upath, min_cost = row_min_cost(a - 1, b, "u", total_cost, min_cost, call_c, costs, matrix)
                ucost = ucost + cost
                upath.append((a, b))
                if call_c != 1:
                    checking.append(ucost)
        except ValueError:
            pass
        try:
            if last != "u":  # Go down (If last command wasn't "Go Up")
                if a + 1 < len(matrix):
                    dcost, dpath, min_cost = row_min_cost(a + 1, b, "d", total_cost, min_cost, call_c, costs, matrix)
                    dcost = dcost + cost # Cost from down side
                    dpath.append((a, b))
                    if call_c != 1:
                        checking.append(dcost)
        except ValueError:
            pass
        try:
            if last != "r" and b - 1 >= 0:  # Go left
                lcost, lpath, min_cost = row_min_cost(a, b - 1, "l", total_cost, min_cost, call_c, costs, matrix)
                lcost = lcost + cost
                lpath.append((a, b))
                if call_c != 1:
                    checking.append(lcost)
        except (ValueError):
            pass

        min_path_dict = dict()
        try:
            min_path_dict[rcost] = rpath
        except UnboundLocalError:
            pass
        try:
            min_path_dict[ucost] = upath
        except UnboundLocalError:
            pass
        try:
            min_path_dict[dcost] = dpath
        except UnboundLocalError:
            pass
        try:
            min_path_dict[lcost] = lpath
        except UnboundLocalError:
            pass
    #   I used try-except statements here because sometimes ucost, dcost, rcost or lcost may not be defined.
    #   If some of those variables are not defined, I still want the code to calculate the minimum value of the
    # ones that are defined.

    # I used a dictionary here so I could return the corresponding path for the minimum cost
    # There won't be an issue for multiples of the same key because I made sure to return a value bigger than the
    #  current minimum if total costs are the same. (cost + 1)


    if call_c == 1: # The return statement for the first call of the function is different.
        min_list = []
        try:
            min_list.append(ucost)
        except UnboundLocalError:
            pass
        try:
            min_list.append(rcost)

        except UnboundLocalError:
            pass
        try:
            min_list.append(dcost)

        except UnboundLocalError:
            pass
        if not min_list:
            raise ValueError

        return min(min_list), min_path_dict[min(min_list)], min_cost
    else:
        return min(checking), min_path_dict[min(checking)], min_cost
        # For each recursion the min of rcost, lcost, ucost, dcost will be returned with the corresponding path
        # and the current minimum cost.


# find_final_min_cost calculates the minimum cost starting from the left of each row and determines the min cost and
# path for the matrix.

def find_final_min_cost(matrix,costs, f_out):
    cost3 = costs[2]
    cost_list = []
    temp_dict = dict() # This dictionary is again for determining the corresponding path for the minimum cost.
    min_cost = len(matrix) * len(matrix[0]) * cost3  # Assigning the max value for min_cost at the start.
    for a in range(len(matrix)):
        if matrix[a][0] != 0:
            try:
                total_cost, path_list, min_cost2 = row_min_cost(a, 0, 0, 0, min_cost, 0, costs, matrix)
            except ValueError:
                continue
            min_cost = min_cost2
            cost_list.append(total_cost)
            temp_dict[total_cost] = path_list
    if not cost_list: # If the cost_list empty, no possible routes could be calculated.
        f_out.write("There is no possible route!")
    else:
        return min(cost_list), temp_dict[min(cost_list)]
        # Returning the final minimum cost and the path.
        # Path is returned as a list of tuples: [(2,3), (2,2), ... , (0,0)]


def main():
    from sys import argv

    f_in = open(argv[1], "r")
    f_out = open(argv[2], "w")

    costs = f_in.readline().replace("\n", "").split()

    matrix = []

    for i in range(len(costs)):
        costs[i] = int(costs[i])


    # Converting the contents of the input into a matrix of tuples of integers.
    for line in f_in:
        if line == "":
            continue
        else:
            int_line = line.split()
            for i in range(len(int_line)):
                int_line[i] = int(int_line[i])
            matrix.append(int_line)

    try:
        final_min_cost, min_path = find_final_min_cost(matrix,costs, f_out)

        f_out.write("Cost of the route: {}".format(final_min_cost))

        for a in range(len(matrix)):
            for b in range(len(matrix[a])):
                if (a,b) in min_path:
                    matrix[a][b] = "X" # Replacing the boxes that were stepped on with X's.
        for i in matrix:
            print_str = str(i).replace("'", "").replace(",", "").replace("[",
                                                                         "").replace("]", "")
            f_out.write("\n{}".format(print_str))
    except TypeError:
        # If there is no possible route find_final_min_cost will return None so the first line in this block will
        # raise a TypeError.
        pass
if __name__ == "__main__":
    main()
