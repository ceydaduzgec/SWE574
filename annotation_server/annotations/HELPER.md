
1.2 Serialization of the Model

When the only information that is recorded in the annotation is the IRI of a resource, then that IRI is used as the value of the relationship, as in Example 1. When there is more information about the resource, the IRI is the value of the id property of the object which is the value of the relationship, as in Example 2.

1.4 Terminology
IRI
An IRI, or Internationalized Resource Identifier, is an extension to the URI specification to allow characters from Unicode, whereas URIs must be made up of a subset of ASCII characters. There is a mapping algorithm for translating between IRIs and the equivalent encoded URI form. IRIs are defined by [rfc3987].
Resource
An item of interest that may be identified by an IRI.
Web Resource
A Resource that must be identified by an IRI, as described in the Web Architecture [webarch]. Web Resources may be dereferencable via their IRI.
External Web Resource
A Web Resource which is not part of the representation of the Annotation, such as a web page, image, or video. External Web Resources are dereferencable from their IRI.
Property
A feature of a Resource, that often has a particular data type. In the model sections, the term "Property" is used to refer to only those features which are not Relationships and instead have a literal value such as a string, integer or date. The valid values for a Property are thus any data type other than object, or an array containing members of that data type if more than one is allowed.
Relationship
In the model sections, the term "Relationship" is used to distinguish those features that refer to other Resources, either by reference to the Resource's IRI or by including a description of the Resource in the Annotation's representation. The valid values for a Relationship are: a quoted string containing an IRI, an object that has the "id" property, or an array containing either of these if more than one is allowed.
Class
Resources may be divided, conceptually, into groups called "classes"; members of a class are known as Instances of the class. Resources are associated with a particular class through typing. Classes are identified by IRIs, i.e., they are also Web Resources themselves.
Type
A special Relationship that associates an Instance of a class to the Class it belongs to.
Instance
An element of a group of Resources represented by a particular Class.


2. Web Annotation Principles

Annotations have 0 or more Bodies.
Annotations have 1 or more Targets.


Annotations, Bodies and Targets may have their own properties and relationships, typically including creation and descriptive information.
