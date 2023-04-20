use rand::Rng; // 0.8.0
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let mut counter = 0;
    let mut rng = rand::thread_rng();

    let result = loop {
        counter += 1;
        if counter % 100 == 0 {
            println!("processed {} records", counter);
            sleep(Duration::from_millis(100)).await;
        }
        if rng.gen_range(0..5000) == 0 {
            panic!("Encountered error {}", counter);
        }

        if counter == 5000 {
            break counter;
        }
    };
    assert_eq!(result, 5000);
    println!("Done!");
}