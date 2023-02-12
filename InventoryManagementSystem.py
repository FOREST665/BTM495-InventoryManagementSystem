from typing import List # for list type hints

class User:
    # create the new user
    def __init__(self, userName, employeeID, email, role):
        self.userName = userName
        self.employeeID = employeeID
        self.email = email
        self.role = role

    # ------ Modify the user  -----
    def setName(self, newName):
        self.userName = newName

    def setEmail(self, newEmail):
        self.email = newEmail

    def setEmployeeID(self, newEmployeeID):
        self.employeeID = newEmployeeID

    def setRole(self, newRole):
        self.role = newRole

class Product:
    def __init__(self, type, productName, productID, price, quantity):
        self.productName = productName
        self.type = type
        self.productID = productID
        self.price = price
        self.quantity = quantity

    def setProductName(self, newProductName):
        self.productName = newProductName

    def setProductType(self, newType):
        self. type = newType

    def setProductID(self, newProductID):
        self.productID = newProductID
    
    def setQuantity(self, newQuantity):
        self.quantity = newQuantity

class LineItem:
    def __init__(self, product: Product, quantity):
        self.product = product
        self.quantity = quantity

    def setQuantity(self, newQuantity):
        self.quantity = newQuantity


class Supplier:
    def __init__(self, supplierID, companyName, phone, supplierEmail, contact, location, product, invoices):
        self.supplierID = supplierID
        self.companyName = companyName
        self.phone = phone
        self.supplierEmail = supplierEmail
        self.contact = contact
        self.location = location
        self.product = product
        if len(invoices) == 0:
            raise Exception("An order must be associated with at least one invoice!")
        self.invoices = invoices

    def setSupplierID(self, newSupplierID):
        self.supplierID = newSupplierID
    
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
    def __init__(self, order, type, reason, supplier: Supplier):
        self.invoiceNumber = nextInvoiceNumber
        nextInvoiceNumber += 1

        self.order = order
        self.invoiceTotal = order.calculateOrderTotal()
        self.type = type
        self.reason = reason
        self.supplier = supplier

    def setType(self, newType):
        self.type = newType
    
    def setReason(self, newReason):
        self.reason = newReason


class Order:
    def __init__(self, users: List[User], lineItems: List[LineItem], orderID, date, deliveryDate):

        if len(users) == 0:
            raise Exception("An order must be associated with at least one user!")
        if len(lineItems) == 0:
            raise Exception("An order must be associated with at least one line item!")
        
        self.users = users
        self.lineItems = lineItems
        self.orderID = orderID
        self.date = date
        self.deliveryDate = deliveryDate


    def setOrderID(self,newOrderID):
        self.orderID = newOrderID
    
    def setDate(self, newDate):
        self.date = newDate
    
    def setDeliveryDate(self, newDeliveryDate):
        self.deliveryDate = newDeliveryDate


    def addLineItem(self, lineItem):
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
    def __init__(self, products: List[Product]):
        self.products = products
    
    def findProductByName(self, productNameToFind):
        for product in self.product:
            if product.productName == productNameToFind:
                return product
        return None

    def addProductToInventory(self, type, productName, productID, price ):
        self.products.append(Product(type, productName, productID, price))
    
    def removeProductFromInventory(self, product: Product):
        self.products.remove(product)

    
class InventoryManagementSystem:
    def __init__(self):
        self.users = []
        self.suppliers = []
        self.invoices = []


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

    def addSupplier(self, supplierID, companyName, phone, supplierEmail, contact, location, product):
        self.suppliers.append(Supplier(supplierID, companyName,phone,supplierEmail,contact,location,product))

    def removeSupplierByName(self, companyName):
        self.suppliers.remove(self.findSupplierByName(companyName))


def main():
    ... #TODO
