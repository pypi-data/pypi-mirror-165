import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.given_value_list = [2]
        self.given_value_offset = [-0.46]
        self.attach_list = [1, 5, 8]
        self.attach_list_amend = [3., 6., 9.]

        self.result = [2.54, 6.0, 9.0]

    def test_something(self):
        print(self.attach_list, self.attach_list_amend)

        def myfunc(given_value_list, given_value_offset, attach_list, attach_list_amend):
            for given_value, give_offset in zip(given_value_list, given_value_offset):
                print(f"{given_value} {give_offset}")
                closest_value = min(attach_list, key=lambda list_value: abs(list_value - given_value))
                nearest_given_index = attach_list.index(closest_value)
                print(f"closest_value {closest_value} nearest_given_index{nearest_given_index}")
                attach_list_amend[nearest_given_index] += give_offset

        myfunc(self.given_value_list,
               self.given_value_offset,
               self.attach_list,
               self.attach_list_amend)

        print(self.attach_list, self.attach_list_amend)

        for index, item in enumerate(self.attach_list_amend):
            self.assertEqual(item, self.result[index])


if __name__ == '__main__':
    unittest.main()
