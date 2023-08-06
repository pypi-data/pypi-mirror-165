import unittest
import pathlib
import numpy as np

# Get location of this file
__this_file__ = pathlib.Path(__file__)
__this_path__ = __this_file__.parent.resolve()

# Get path to input to test data
test_data_path = __this_path__.joinpath('test_data')
test_data_file = test_data_path.joinpath('test_database.tim')
verification_data_file = test_data_path.joinpath('test_data_actuals.npz')

test_data_file_2 = test_data_path.joinpath('test_database_2.tim')
test_data_file_3 = test_data_path.joinpath('test_database_3.tim')


__create_actuals_data_file__ = False


class TestStringMethods(unittest.TestCase):

    @classmethod
    def buildUpClass(cls) -> None:
        # Runs once before all test
        print(' Perform setup of test environment')
        numpy_export_file = test_data_file.with_suffix('.npz')
        if numpy_export_file.is_file():
            # Cleanup temporary _file
            numpy_export_file.unlink()
            print(f' Cleanup completed of: {numpy_export_file.as_posix()} ')

    @classmethod
    def tearDownClass(cls) -> None:
        # Runs once after all test
        print(' Perform tear down/cleaning of test environment')
        numpy_export_file = test_data_file.with_suffix('.npz')
        if numpy_export_file.is_file():
            # Cleanup temporary _file
            numpy_export_file.unlink()
            print(f' Cleanup completed of: {numpy_export_file.as_posix()} ')

    def test_001_read_rpc_file(self):
        """
            Test reading of rpc data
        """
        from rpc_reader.rpc_reader import ReadRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ReadRPC(test_data_file, debug=False)

        # Import data from rpc _file
        data_object.import_rpc_data_from_file()

        # Print header data
        data_object.print_channel_header_data()

        # Get data size
        samples, channels = data_object.get_data_size()

        data = data_object.get_data()
        print(f'\n\t Read data shape: {data.shape}')

        time, test_end_time = data_object.get_time()

        print(f'\n Test data points read:\n\tChannels: {channels}'
              f'\n\tSamples:  {samples}'
              f'\n\tDuration: {np.round(test_end_time, 4)} seconds')
        self.assertTrue(True)

    def test_002_read_rpc_file_extra_headers(self):
        """
            Test reading of rpc data with additional headers supplied
        """
        extra_headers = [['DATA_TYPE', 'SHORT_INTEGER'],
                         ['NON_EXISTING_HEADER', 'CUSTOM_LABEL']]

        from rpc_reader.rpc_reader import ReadRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ReadRPC(test_data_file, extra_headers=extra_headers, debug=True)

        # Import data from rpc _file
        data_object.import_rpc_data_from_file()

        # Print header data
        data_object.print_channel_header_data()

        # Get data size
        samples, channels = data_object.get_data_size()

        data = data_object.get_data()
        print(f'\n\t Read data shape: {data.shape}')

        time, test_end_time = data_object.get_time()

        print(f'\n Test data points read:\n\tChannels: {channels}'
              f'\n\tSamples:  {samples}'
              f'\n\tDuration: {np.round(test_end_time, 4)} seconds')
        self.assertTrue(True)

    def test_003_export_rpc_data(self):
        """
            Test export of npz data
        """
        from rpc_reader.rpc_reader import ReadRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ReadRPC(test_data_file)
        # Read data from file
        data_object.import_rpc_data_from_file()

        # Export data
        data_object.save_npy_data_to_file(overwrite=True)

        self.assertTrue(True)

    def test_004_import_rpc_data(self):
        """
            Test import of npz data
        """
        from rpc_reader.rpc_reader import ReadRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ReadRPC(test_data_file)

        # Import data
        data_object.import_npy_data_from_file()

        self.assertTrue(True)

    def test_005_verify_csv(self):
        """
            Compare data read data with csv data exported from RPC Pro
        """

        from rpc_reader.rpc_reader import ReadRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ReadRPC(test_data_file)

        # Import data
        data_object.import_npy_data_from_file()

        # Code uses for generation of actual data file from csv data not included in repo
        if __create_actuals_data_file__:
            # Read csv data
            with open(verification_data_file, 'r') as f:
                verification_csv_data = f.readlines()

            # Pre-allocate storage
            verification_csv = np.zeros((len(verification_csv_data), 32))

            # Store data in file
            for no, line in enumerate(verification_csv_data):
                verification_csv[no, :] = np.array(line.split(), dtype=np.float32)

            np.savez_compressed(verification_data_file.with_suffix('.npz'),
                                verification_csv=verification_csv)

        # Load csv data from pickle file
        npz_file = np.load(verification_data_file.with_suffix('.npz'), allow_pickle=True)
        csv_data = npz_file['verification_csv']

        # Compare data RPC Pro and read data. It will not be identical due to different accuracy of float representation
        equal = np.allclose(csv_data, data_object.data, atol=0.0001, rtol=0.001)

        # Assert the result of the comparison
        self.assertTrue(equal, msg=' All values were not equal')

    def test_102_progressbar(self):
        """
            Test reading of rpc data
        """
        from rpc_reader.lib.print_progressbar import print_progressbar
        import time
        total = 100
        print_progressbar(0, total, prefix='Progress:', suffix='Complete', length=50)
        for i in range(total):
            # Do stuff...
            time.sleep(0.01)
            # Update Progress Bar
            print_progressbar(i + 1, total, prefix='Progress:', suffix='Complete', length=50)
        self.assertTrue(True)

    def test_301_read_rpc_file_2(self):
        """
            Test reading of rpc data - Test file 2
        """
        from rpc_reader.rpc_reader import ReadRPC
        print(f' Reading data from file: \n\t{test_data_file_2.as_posix()}\n')

        # Instantiate instance
        data_object = ReadRPC(test_data_file_2, debug=False)

        # Import data from rpc _file
        data_object.import_rpc_data_from_file()

        # Print header data
        data_object.print_channel_header_data()

        # Get data size
        samples, channels = data_object.get_data_size()

        data = data_object.get_data()
        print(f'\n\t Read data shape: {data.shape}')

        time, test_end_time = data_object.get_time()

        print(f'\n Test data points read:\n\tChannels: {channels}'
              f'\n\tSamples:  {samples}'
              f'\n\tDuration: {np.round(test_end_time, 4)} seconds')
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
