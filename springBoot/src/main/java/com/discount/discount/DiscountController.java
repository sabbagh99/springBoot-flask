package com.discount.discount;


import jdk.nashorn.internal.parser.JSONParser;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.net.HttpURLConnection;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Scanner;

@RestController
public class DiscountController {


    @RequestMapping("/hi")
    @ResponseBody
    String homee() throws URISyntaxException {
        try {
            RestTemplate restTemplate = new RestTemplate();

            String url = "http://192.168.43.142:5000/";
            String productNameResult = restTemplate.getForObject(url, String.class);
            SimpleClientHttpRequestFactory rf =
                    (SimpleClientHttpRequestFactory) restTemplate.getRequestFactory();
            rf.setReadTimeout(1 * 1000);
            rf.setConnectTimeout(1 * 1000);
            return productNameResult;

        } catch (Exception e) {
            e.printStackTrace();
        }
        return "productNameResult";
    }

    @GetMapping("/")
    String home() throws URISyntaxException {
        try {
            URL url = new URL("http://192.168.43.142:5000/");

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();

            //Check if connect is made
            int responseCode = conn.getResponseCode();

            if (responseCode != 200) {
                throw new RuntimeException("HttpResponseCode: " + responseCode);
            } else {

                StringBuilder informationString = new StringBuilder();
                Scanner scanner = new Scanner(url.openStream());

                while (scanner.hasNext()) {
                    informationString.append(scanner.nextLine());
                }
                scanner.close();


                return String.valueOf(informationString);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

//    @GetMapping("/mobiles/productinfo")
//    public List<Product> getProductsInfo() {
//        List<Product> productList = new ArrayList();
//        try {
//
//            SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory ();
//            requestFactory.setConnectTimeout(10 * 1000);
//            requestFactory.setReadTimeout(10 * 1000);
//            RestTemplate restTemplate = new RestTemplate(requestFactory);
//            Product product = null;
//            String productName = "http://127.0.0.1:5000/mobiles/productName?oneplus=false&apple=true";
//            String productPrice = "http://127.0.0.1:5000/mobiles/productPrice";
//            String productDiscount = "http://127.0.0.1:5000/mobiles/productDiscount";
//            String productSite = "http://127.0.0.1:5000/mobiles/productSite";
//            String productNameResult = restTemplate.getForObject(productName, String.class);
//            String productPriceResult = restTemplate.getForObject(productPrice, String.class);
//            String productDiscountResult = restTemplate.getForObject(productDiscount, String.class);
//            String productSiteResult = restTemplate.getForObject(productSite, String.class);
//            List<String> productNameList = Arrays.asList(productNameResult.split("\\s*~\\s*"));
//            List<String> productPriceList = Arrays.asList(productPriceResult.split("\\s*~\\s*"));
//            List<String> productDiscountList = Arrays.asList(productDiscountResult.split("\\s*~\\s*"));
//            List<String> productSiteList = Arrays.asList(productSiteResult.split("\\s*~\\s*"));
//
//            for (int i = 0; i < productNameList.size(); i++) {
//                product = new Product(1, productNameList.get(i), 0d, (productPriceList.get(i)), (productDiscountList.get(i)), "", productSiteList.get(i));
//                productList.add(product);
//            }
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        return productList;
//    }


}
