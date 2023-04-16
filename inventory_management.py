
from typing import List # for list type hints

class User:
    # create the new user
    def __init__(self, userName, employeeID, email, role):
        self.userName = userName
        self.employeeID = employeeID
        self.email = email
        self.role = role
        self.orders = []

    # ------ Modify the user  -----
    def setName(self, newName):
        self.userName = newName

    def setEmail(self, newEmail):
        self.email = newEmail

    def setEmployeeID(self, newEmployeeID):
        self.employeeID = newEmployeeID

    def setRole(self, newRole):
        self.role = newRole

    def createPurchaseOrder(self, lineItems, orderDate, deliveryDate):
        self.orders.append(Order([self], lineItems, orderDate, deliveryDate))


class Product:
    nextProductId = 0
    def __init__(self, type, productName, price, quantity, reorderPoint):
        self.productName = productName
        self.type = type
        self.productID = Product.nextProductId
        Product.nextProductId += 1
        self.price = price
        self.quantity = quantity
        self.reorderPoint = reorderPoint

    def setProductName(self, newProductName):
        self.productName = newProductName

    def setProductType(self, newType):
        self. type = newType

    def setProductID(self, newProductID):
        self.productID = newProductID
    
    def setQuantity(self, newQuantity):
        self.quantity = newQuantity

    def setReorderPoint(self, newReorderPoint):
        self.reorderPoint = newReorderPoint
    
    
    def linkSupplierToProduct(self, newSupplier):
        self.supplier= newSupplier

    def unlinkSupplierToProduct(self):
        self.supplier= None
    

class LineItem:
    def __init__(self, product: Product, quantity):
        self.product = product
        self.quantity = quantity

    def setQuantity(self, newQuantity):
        self.quantity = newQuantity


class Supplier:
    nextSupplierID = 0
    def __init__(self, companyName, phone, supplierEmail, contact, location, product, invoices):
        self.supplierID = Supplier.nextSupplierID
        Supplier.nextSupplierID += 1
        self.companyName = companyName
        self.phone = phone
        self.supplierEmail = supplierEmail
        self.contact = contact
        self.location = location
        self.product = product
        self.invoices = invoices
    
    def setCompanyName(self, newCompanyName):
        self.companyName = newCompanyName

    def setPhone(self, newPhone):
        self.phone = newPhone

    def setSupplierEmail(self, newSupplierEmail):
        self.supplierEmail = newSupplierEmail

    def setContact(self, newContact):
        self.contact = newContact

    def setLocation(self, newlocation):
        self.location = newlocation

    def setProduct(self, newProduct):
        self.product = newProduct



class Invoice:
    nextInvoiceNumber = 0
    def __init__(self, order, type, supplier: Supplier):
        self.invoiceNumber = Invoice.nextInvoiceNumber
        Invoice.nextInvoiceNumber += 1

        self.order = order
        self.invoiceTotal = order.calculateOrderTotal()
        self.type = type
        self.deliveryReason = ""
        self.supplier = supplier

        self.deliveryStatus = "Not Delivered"

    def setType(self, newType):
        self.type = newType
    
    def addDeliveryReason(self, newDeliveryReason):
        self.deliveryReason = newDeliveryReason

    def addDeliverySatus(self, newDeliveryStatus):
        self.deliverStatus = newDeliveryStatus


class Order:
    nextOrderID = 0
    def __init__(self, users: List[User], lineItems: List[LineItem], orderDate, deliveryDate):

        if len(users) == 0:
            raise Exception("An order must be associated with at least one user!")
        if len(lineItems) == 0:
            raise Exception("An order must be associated with at least one line item!")
        
        self.users = users
        self.lineItems = lineItems
        self.orderID = Order.nextOrderID
        Order.nextOrderID += 1
        self.orderDate = orderDate
        self.deliveryDate = deliveryDate

    def setDate(self, newDate):
        self.date = newDate
    
    def setDeliveryDate(self, newDeliveryDate):
        self.deliveryDate = newDeliveryDate

    def addLineItem(self, lineItem: LineItem):
        self.lineItems.append(lineItem)

    def removeLineItemByProductName(self, productName):
        for lineItem in self.lineItems:
            if lineItem.product.productName == productName:
                self.lineItems.remove(lineItem)
                return
    def findLineItemByProductName(self, productName):
        for lineItem in self.lineItems:
            if lineItem.product.productName == productName:
                return lineItem
        return None
 
    def calculateOrderTotal(self):
        total = 0
        for lineItem in self.lineItems:
            total += lineItem.quantity * lineItem.product.price

        return total
    
    def createInvoiceForOrder(self, supplier: Supplier, invoiceReason, type):
        self.invoice = Invoice(self, type, invoiceReason, supplier)
        return self.invoice
        

class Inventory:
    def __init__(self):
        self.products: List[Product] = []
    
    def findProductByName(self, productNameToFind) -> Product:
        for product in self.products:
            if product.productName == productNameToFind:
                return product
        return None

    def addProductsToInv(self, type, productName, price, quantity, reorderPoint ):
        self.products.append(Product(type, productName, price, quantity, reorderPoint))
    
    def removeProductFromInv(self, productName):
        self.products.remove(self.findProductByName(productName))

    def lowStockAlert(self):
        lowStockProducts = []
        for product in self.products:
            if product.quantity <= product.reorderPoint:
                print (product.productName+" is low!")
                lowStockProducts.append(product.productName)
        print ("Inventory levels are good")
        return lowStockProducts



    def addQuantityToInventory(self, productName, quantity):
        product = self.findProductByName(productName)
        if product == None:
            print("Error, could not find product " + productName)
            return
        
        product.setQuantity(product.quantity + quantity)

    def removeQuantityFromInventory(self, productName, quantity):
        product = self.findProductByName(productName)

        if product == None:
            print("Error, could not find product " + productName)
            return
        if product.quantity < quantity:
            print("Error: trying to remove quantity from a product that doesn't have enough stock!")
            return
        product.setQuantity(product.quantity - quantity)
        
    
class InventoryManagementSystem:
    def __init__(self):
        self.users = []
        self.suppliers = []
        self.invoices = []
        self.inventory = Inventory()
        self.savedPlacedOrders: List[Order] = []


    def addUser(self, userName, employeeID, email, role):
        self.users.append(User(userName, employeeID, email, role))

    def findUserByName(self, userNameToFind):
        for user in self.users:
            if user.userName == userNameToFind:
                return user
        return None

    def findInvoiceByNumber(self, invoiceToFind):
        for invoice in self.invoices:
            if invoice.invoiceNumber == invoiceToFind:
                return invoice
        return None

    def removeUserByName(self, userName):
        self.users.remove(self.findUserByName(userName))

    def findSupplierByName(self, companyNameToFind):
        for supplier in self.suppliers:
            if supplier.companyName == companyNameToFind:
                return supplier
        return None

    def addSupplier(self, companyName, phone, supplierEmail, contact, location, product, invoices):
        self.suppliers.append(Supplier(companyName,phone,supplierEmail,contact,location,product, invoices))

    def removeSupplierByName(self, companyName):
        self.suppliers.remove(self.findSupplierByName(companyName))


    def getInventory(self):
        return self.inventory

    def savedInvoices(self, invoice):
        self.invoices.append(invoice)

    def removeSavedInvoices(self, invoiceNumber):
        self.invoices.remove(self.findInvoiceByNumber(invoiceNumber))
        
    def savePlacedOrders(self, order: Order):
        self.savedOrders.append(order)

    def findOrderByID(self, orderIdToFind):
        for savedOrder in self.savedPlacedOrders:
            if savedOrder.orderID == orderIdToFind:
                return savedOrder
        return None
        
    def findExpectedDeliveryByOrder(self,orderIdToFind):
        order = self.findOrderByID(orderIdToFind)
        if order != None:
            return order.deliveryDate
            
        print("Error: Tried to find expected delivery date for order which does not exist!")
        return ""


    def removePlacedOrders(self, orderId):
        self.orders.remove(self.findOrderByID(orderId))


# Test code below:

def testManageOrder():
    print("Running Manage Order Test...")
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()
    ims.addSupplier("The milk people", "5146395282", "sarah@ims.com", "Sarah","Brossard","The Thirsty Cow", [])

    inventory = ims.getInventory()
    inventory.addProductsToInv("Milk", "The Thirsty Cow", 3.99, 5, 2)



    supplier = ims.findSupplierByName("The milk people")
    if supplier == None:
        print("Error, cannot find supplier 'The milk people'!")
        return False

    product = inventory.findProductByName("The Thirsty Cow")
    if product == None:
        print("Error, could not find product 'The Thirsty Cow'")
        return False

    lineItem = LineItem(product, 2)
    order = Order([supplier], [lineItem], "April 14, 2023", "April 16th, 2023")

    # validate that the order total is what we expect:

    if order.calculateOrderTotal() != (3.99 * 2):
        print("Error, expected a different order total")
        return False


    return True


def testManageOrderNoSupplier():
    print("Running Manage Order No Supplier Test...")
    
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()

    inventory = ims.getInventory()
    inventory.addProductsToInv("Milk", "The Thirsty Cow", 3.99, 5, 2)


    # Start testing the manage order sequence

    supplier = ims.findSupplierByName("The milk people")
    if Supplier == None:
        return True
    else:
        print("Found a supplier when none was expected!")
        return False


def testManageOrderNoProduct():
    print("Running Manage Order No Product Test...")
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()
    ims.addSupplier("The milk people", "5146395282", "sarah@ims.com", "Sarah","Brossard","The Thirsty Cow", [])

    inventory = ims.getInventory()
    
    # Start testing the manage order sequence 

    Supplier = ims.findSupplierByName("The milk people")
    if Supplier == None:
        print("Error, cannot find supplier 'The milk people'!")
        return False

    product = inventory.findProductByName("The Thirsty Cow")
    if product != None:
        print("Error, found product which should not exist 'The Thirsty Cow'")
        return False
    
    return True

def testAddProduct():
    print("Running Add Product test...")
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()
    
    inventory = ims.getInventory()

    product = inventory.findProductByName("The detox blend")
    if product != None:
        print("Error, found product which should not exist 'The detox blend'")
        return False

    inventory.addProductsToInv("black tea", "The detox blend", 6.25, 9, 3)

    product = inventory.findProductByName("The detox blend")
    if product == None:
        print("Error, found product which should not exist 'The detox blend'")
        return False

    return True

def testRemoveProduct():
    print("Running Remove Product test...")
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()

    inventory = ims.getInventory()

    inventory.addProductsToInv("black tea", "The detox blend", 6.25, 9, 3)

    product = inventory.findProductByName("The detox blend")
    if product == None:
        print("Error, couldn't find product which we expect to exist: 'The detox blend'")
        return False
    
    inventory.removeProductFromInv("The detox blend")

    product = inventory.findProductByName("The detox blend")
    if product != None:
        print("Error, found product which should not exist because we just removed it: 'The detox blend'")
        return False
    
    return True
   
def testTrackInventoryUnder():
    print("Running track inventory test...")
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()

    inventory = ims.getInventory()

    inventory.addProductsToInv("black tea", "The detox blend", 6.25, 9, 3)
    inventory.addProductsToInv("milk","The Thirsty Cow", 3.99, 5, 2)
    inventory.addProductsToInv("cups","medium cups",0.20, 20,40)

    lowStockProducts = inventory.lowStockAlert()
    
    if len(lowStockProducts) != 1:
        print("Error: expected a single low stock product but got " + len(lowStockProducts) + "!")
        return False
    
    if lowStockProducts[0] != "medium cups":
        print("Error: the low stock alert returned the wrong product name: " + lowStockProducts)
        return False
    
    return True

def testTrackInventoryOver():
    print("Running track inventory test...")
    # setup the IMS to begin testing
    ims = InventoryManagementSystem()

    inventory = ims.getInventory()

    inventory.addProductsToInv("black tea", "The detox blend", 6.25, 9, 3)
    inventory.addProductsToInv("milk","The Thirsty Cow", 3.99, 5, 2)
    inventory.addProductsToInv("cups","medium cups",0.20, 60,40)

    lowStockProducts = inventory.lowStockAlert()
    
    if len(lowStockProducts) != 0:
        print("Error: expected no low stock product but got " + len(lowStockProducts) + "!")
        return False
    
    return True       




def runTests():
    if testManageOrder():
        print("Manage Order Tests Passed!")
    else:
        print("Manage Order Tests Failed!")

    if testManageOrderNoSupplier():
        print("Manage Order Tests No Supplier Passed!")
    else:
        print("Manage Order Tests No Supplier Failed!")

    if testManageOrderNoProduct():
        print("Manage Order Tests No Product Passed!")
    else:
        print("Manage Order Tests No Product Failed!")

    if testAddProduct():
        print("Add Product Tests Passed!")
    else:
        print("Add Product  Tests Failed!")

    if testRemoveProduct():
        print("Remove Product Tests Passed!")
    else:
        print("Remove Product Tests Failed!")

    if testTrackInventoryUnder():
        print("Track Inventory Under Tests Passed!")
    else:
        print("Track Inventory Under Tests Failed!")

    if testTrackInventoryOver():
        print("Track Inventory Over Tests Passed!")
    else:
        print("Track Inventory Over Tests  Failed!")




# this runs the test code if you run the command `python inventory_management.py`
if __name__ == "__main__":
    runTests()
