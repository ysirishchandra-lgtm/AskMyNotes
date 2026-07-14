class Employee {
    String name;
    int age;
    long mdn;

    // default constructor
    Employee() {
        System.out.println("CONSTRUCTOR CREATED");
        name = "SIRISH";
        age = 18;
        mdn = 63010324L;
    }

    // constructor with one parameter
    Employee(String pname) {
        System.out.println("Constructor with one param");
        name = pname;
    }

    // constructor with two parameters
    Employee(String pname, int page) {
        System.out.println("Constructor with two params");
        name = pname;
        age = page;
    }

    // constructor with three parameters
    Employee(String pname, int page, long pmdn) {
        System.out.println("Constructor with three params");
        name = pname;
        age = page;
        mdn = pmdn;
    }

    void develop_App() {
        System.out.println("Develop App called");
    }

    void test_App() {
        System.out.println("Test App called");
    }
}

public class EmployeeDemo {
    public static void main(String[] args) {
        System.out.println("Hello world!!!");

        Employee eobj;
        eobj = new Employee();
        eobj.test_App();
        eobj.develop_App();

        System.out.println("Name:" + eobj.name);
        System.out.println("Age: " + eobj.age);
        System.out.println("MDN: " + eobj.mdn);

        System.out.println();
        Employee eobj2 = new Employee("Priya");
        System.out.println("Name:" + eobj2.name);

        System.out.println();
        Employee eobj3 = new Employee("Amit", 30, 9876543210L);
        System.out.println("Name:" + eobj3.name);
        System.out.println("Age: " + eobj3.age);
        System.out.println("MDN: " + eobj3.mdn);
    }
}
