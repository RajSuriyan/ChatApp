import java.util.Arrays;

class Main {
    public static int[] arr = {1, 2, 34, 7, 6, 2, 6, 8, 9, 5, 756, 6, 8, 5, 435, 43, 6, 57, 654};

    static void merge_sort(int[] arr, int l, int r) {
        if (r - l > 1) {
            int mid = (l + r) / 2;
            merge_sort(arr, l, mid);
            merge_sort(arr, mid, r);
            merge(l, r, mid, arr);
        }
    }

    static void merge(int l, int r, int mid, int[] arr) {
        int i = 0, j = 0, k = l;
        int[] left = Arrays.copyOfRange(arr, l, mid);
        int[] right = Arrays.copyOfRange(arr, mid, r);

        while (i < mid - l && j < r - mid) {
            if (left[i] < right[j]) {
                arr[k] = left[i];
                i++;
            } else {
                arr[k] = right[j];
                j++;
            }
            k++;
        }

        while (i < mid - l) {
            arr[k] = left[i];
            i++;
            k++;
        }

        while (j < r - mid) {
            arr[k] = right[j];
            j++;
            k++;
        }
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(arr));
        merge_sort(arr, 0, arr.length);
        System.out.println(Arrays.toString(arr));
    }
}
