#------------------------------------------#
# Title: CDInventory.py
# Desc: Assignment 06 - Working with classes and functions.
# Change Log: (Who, When, What)
# BAnson, 2020-Aug-16, Created File
# BAnson, 2020-Aug-16, moved write to file code to write_file function
#   Added try-except block to create new file if none exists
#   Cleaned up formatting in I/O presentation
#   Added data processing functions add_data and del_id
#   Added IO functions to collect user inputs of new_id, new_title, new_artist
# BAnson, 2020-Aug-18, removed calls to IO class from DataProcessor class in add_data()
#   Consolidated 3 user input IO functions into 1 get_data()
#   Added:
#       Review of entered data and y/n choice to add to table
#       "are you sure?" to exit sequence
#------------------------------------------#

# -- DATA -------------------------------------------------------------------- #

strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object



# -- PROCESSING FUNCTIONS ---------------------------------------------------- #

class DataProcessor:
    # Added functions for processing
    @staticmethod
    def add_data(strID, strTitle, strArtist):
        """Appends Inventory with values assigned to strID, strTitle, and strArtist
        
        Args:
            strID = user input ID
            strTitle = user input Title
            strArtist = user input Artist
            
        Returns:
            Integer version of strID (intID)
            A dictionary row (dictRow) containing intID, strTitle, strArtist
            
        """

        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        
    @staticmethod
    def del_id():
        """Deletes CD inventory item based on ID
        
        Args:
            None
            
        Returns:
            None
            
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Writes data in memory table to a text file (or creates empty text file if none exists
        
        Args:
            file_name = name of the file to open and write data to (or create)
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            Text file containing data of current table in memory
        """
        
        # Moved this code from while loop menu 's'
        objFile = open(strFileName, 'w')
        for row in lstTbl:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) FUNCTIONS ----------------------------------- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selectioni

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
            
        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')

    # added I/O functions:
    
    @staticmethod
    def get_data():
        """Collects three pieces of data from user: ID, title, and artist
        
        Args:
            None
            
        Returns:
            Tuple containing values corresponding to ID (strID), title (strTitle), and artist (strArtist)
            
        """
        
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        tplUserData = (strID, strTitle, strArtist)
        return tplUserData

        
# -- MAIN PROGRAM ------------------------------------------------------------ #
        

# 1. When program starts, read in the currently saved Inventory, or create empty file
try:
    FileProcessor.read_file(strFileName, lstTbl)
except:
    FileProcessor.write_file(strFileName, lstTbl)
    

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection 
    # 3.1 process exit first
    if strChoice == 'x':
        choice = input('Are you sure you want to exit? [y/n]: ') # prevent exiting accidentally
        if choice.lower() == 'y':
            break
        else:
            continue

    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # Moved IO code into function
        tplUserData = IO.get_data()
        # Review entry
        print('\nYou entered: ', tplUserData)
        choice = input('Continue to add data to table? [y/n]: ')
        if choice.lower() == 'y':
            strID, strTitle, strArtist = tplUserData
            # 3.3.2 Add item to the table
            DataProcessor.add_data(strID, strTitle, strArtist)
            IO.show_inventory(lstTbl)
        else:
            print('Data not added to table.')
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        # Moved processing code into function
        DataProcessor.del_id()
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl) # function call replaces previous code
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




