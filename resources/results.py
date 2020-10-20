from itertools import zip_longest
import json


def results_handler(r_matrix,  m_matrix):

    rows_matrix = r_matrix
    moves_matrix = m_matrix

    # Transposing ROWS MATRX to COLUMN:
    columns_matrix = [list(filter(None, i))
                      for i in zip_longest(*rows_matrix, fillvalue=None)]

    diagonal_reference_1 = [[1, 1], [2, 2], [3, 3]]
    diagonal_reference_2 = [[1, 3], [2, 2], [3, 1]]

    print("Rows Matrix Sorted : " + str(rows_matrix))
    print("Column Matrix Sorted : " + str(columns_matrix))

    for i in range(len(columns_matrix)):
        print("Iteration Number: " + str(i + 1))
        # FIRST CHECK ===> ANY ROW FILLED:
        if len(rows_matrix[i]) == 3 and len(set(rows_matrix[i])) == 3:
            return True
        # SECOND CHECK ===> ANY COLUMN FILLED:
        elif len(columns_matrix[i]) == 3 and len(set(columns_matrix[i])) == 1:
            return True
        # THIRD CHECK ===> ANY DIAGONAL FILLED:
        else:
            if (all(el in moves_matrix for el in diagonal_reference_1)):
                return True
            elif (all(el in moves_matrix for el in diagonal_reference_2)):
                return True

    return False


def parseJSON(dictionary):
    return json.dumps(dictionary, sort_keys=True, indent=4,
                      ensure_ascii=False)


# TESTS >>>
if __name__ == "__main__":
    print("Run your Tests here:\n")
