# -*- coding: utf-8 -*-

Feature: Image sync between regions, choosing the preferable order or regions for synchronization.
  As a sys-admin of FIWARE federation
  I want to sync images from master node to other nodes in the federation using 'custom' properties to keep the sync order
  So that I can use the same base images in all nodes and keep them updated in regions following the preferable order


  @happy_path @env_dependant @experimentation
  Scenario Outline: Sync images following a preferable order (default behaviour).
    Given a new image created in the Glance of master node with name "qatesting20meg"
    And   GlanceSync configured to sync images using these configuration parameters:
            | config_section  | config_key          | config_value           |
            | DEFAULT         | metadata_condition  | 'image.is_public'      |
            | DEFAULT         | metadata_set        |                        |
            | main            | preferable_order    | <preferable_order>     |
    When  I sync images
    Then  all images are synchronized
    And   the timestamp of image "qatesting20meg" in "<node_greater>" is greater than the image in "<node_lesser>"

    Examples:
            | preferable_order       | node_greater | node_lesser |
            | 'Burgos, Caceres'      | Caceres      | Burgos      |
            | 'Caceres, Burgos'      | Burgos       | Caceres     |


  @skip @bug @CLAUDIA-5323 @env_dependant @experimentation
  Scenario Outline: Sync images between different targets, following a preferable order.
    Given a new image created in the Glance of master node with name "qatesting20meg"
    And   GlanceSync configured to sync images using these configuration parameters:
            | config_section  | config_key          | config_value           |
            | DEFAULT         | metadata_condition  | 'image.is_public'      |
            | DEFAULT         | metadata_set        |                        |
            | main            | preferable_order    | <preferable_order>     |
    When  I sync images on "master:Burgos federation2:Madrid"
    Then  all images are synchronized
    And   the timestamp of image "qatesting20meg" in "<node_greater>" is greater than the image in "<node_lesser>"

    Examples:
            | preferable_order             | node_greater | node_lesser |
            | 'Burgos, federation2:Madrid' | Madrid       | Burgos      |
            | 'federation2:Madrid, Burgos' | Burgos       | Madrid      |


  @happy_path @env_dependant @experimentation
  Scenario Outline: Sync images except the configured ones in 'ignore_regions' property.
    Given a new image created in the Glance of master node with name "qatesting01"
    And   GlanceSync configured to sync images using these configuration parameters:
            | config_section  | config_key          | config_value           |
            | DEFAULT         | metadata_condition  | 'image.is_public'      |
            | DEFAULT         | metadata_set        |                        |
            | master          | ignore_regions      | <ignored_region>       |
    When  I sync images
    Then  the image "qatesting01" is synchronized in target node "<other_region>"
    And   the image "qatesting01" is only present in target node "<other_region>"

    Examples:
            | ignored_region  | other_region        |
            | Burgos          | Caceres             |
            | Caceres         | Burgos              |
