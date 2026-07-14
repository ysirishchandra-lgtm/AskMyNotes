import java.util.Scanner;

class FitnessRecord {
    private String name;
    private int stepsWalked;
    private int caloriesBurned;
    private int hoursSlept;

    public FitnessRecord(String name, int stepsWalked, int caloriesBurned, int hoursSlept) {
        this.name = name;
        this.stepsWalked = stepsWalked;
        this.caloriesBurned = caloriesBurned;
        this.hoursSlept = hoursSlept;
    }

    public void displaySummary() {
        System.out.println("----- Fitness Summary -----");
        System.out.println("User Name        : " + name);
        System.out.println("Steps Walked     : " + stepsWalked);
        System.out.println("Calories Burned  : " + caloriesBurned);
        System.out.println("Hours Slept      : " + hoursSlept);
        System.out.println();
        System.out.println(stepGoalMessage());
        System.out.println(sleepMessage());
    }

    public boolean isStepGoalAchieved() {
        return stepsWalked >= 10000;
    }

    public boolean hasHealthySleep() {
        return hoursSlept >= 7;
    }

    private String stepGoalMessage() {
        return isStepGoalAchieved() ? "Step Goal Achieved" : "Step Goal Not Achieved";
    }

    private String sleepMessage() {
        return hasHealthySleep() ? "Healthy Sleep Duration" : "Sleep Duration Below Recommended Level";
    }
}

public class FitTrack {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("Enter User Name:");
            String userName = scanner.nextLine().trim();

            System.out.println();
            System.out.println("Enter Steps Walked:");
            int stepsWalked = Integer.parseInt(scanner.nextLine().trim());

            System.out.println();
            System.out.println("Enter Calories Burned:");
            int caloriesBurned = Integer.parseInt(scanner.nextLine().trim());

            System.out.println();
            System.out.println("Enter Hours Slept:");
            int hoursSlept = Integer.parseInt(scanner.nextLine().trim());

            System.out.println();
            FitnessRecord fitnessRecord = new FitnessRecord(userName, stepsWalked, caloriesBurned, hoursSlept);
            fitnessRecord.displaySummary();

            System.out.println();
            System.out.println("Would you like to enter details for another user? (yes/no)");
            String another = scanner.nextLine().trim().toLowerCase();
            if (!another.equals("yes") && !another.equals("y")) {
                break;
            }
            System.out.println();
        }

        scanner.close();
    }
}
