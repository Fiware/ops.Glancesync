# -*- coding: utf-8 -*-

Feature: Image sync between regions using GlanceSync in the same federation but
  taking into account the metadata value to be synchronized.

  As a sys-admin user,
  I want to check the synchronisation of the metadata of the images in the FIWARE Lab federation
  So that the list of synchronized images has the same metadata values after the operation.

  @happy_path
    Scenario: 01: Sync a public image with correct metadata value
     Given a new image created in the Glance of master node with name "qatesting01" and this properties
             | param_name      | param_value         |
             | is_public       | True                |
             | sdc_aware       | NULL                |
             | type            | fiware:apps         |
             | nid             | 453                 |
     And   GlanceSync configured to sync images using this configuration parameters:
            | config_section  | config_key          | config_value           |
            | DEFAULT         | metadata_condition  | image.is_public        |
            | DEFAULT         | metadata_set        | 'nid, type, sdc_aware' |
     When  I sync the image
     Then  all images are synchronized
     And   the image "qatesting01" is present in all nodes with the expected data
     And   the properties values of the image "qatesting01" in all nodes are the following
             | param_name      | param_value         |
             | sdc_aware       | NULL                |
             | type            | fiware:apps         |
             | nid             | 453                 |


   @skip
    Scenario Outline: 02: Sync public images with incorrect metadata value
     Given a new image created in the Glance of master node with name "qatesting01" and this properties
            | is_public    | sdc_aware    | type    | nid    |
            | <is_public>  | <sdc_aware>  | <type>  | <nid>  |
     And   GlanceSync configured to sync images using this configuration parameters:
            | config_section  | config_key          | config_value           |
            | DEFAULT         | metadata_condition  | image.is_public        |
            | DEFAULT         | metadata_set        | 'nid, type, sdc_aware' |
     When  I sync the image
     Then  no images are synchronized
     And   this error message:"<message>" is shown to the user
            | message                                                                   |
            | The image cannot be synchronized due to the metadata value is not correct |

            Examples:
            | is_public  | sdc_aware  | type        | nid   |
            | True       | fake       | fake        | 45555 |
            | True       | fake       | fake        | fake  |
            | True       | fake       | 1234        | 45555 |
            | True       | fake       | 1234        | fake  |
            | True       | fake       |             | 45555 |
            | True       | fake       |             | fake  |
            | True       | fake       | fiware:apps | 45555 |
            | True       | fake       | fiware:apps | fake  |
            | True       | True       | fake        | 45555 |
            | True       | True       | fake        | fake  |
            | True       | True       | 1234        | 45555 |
            | True       | True       | 1234        | fake  |
            | True       | True       |             | 45555 |
            | True       | True       |             | fake  |
            | True       | True       | fiware:apps | 45555 |
            | True       | True       | fiware:apps | fake  |
            | True       | True       | fake        | 45555 |
            | True       | True       | fake        | fake  |
            | True       | True       | 1234        | 45555 |
            | True       | True       | 1234        | fake  |
            | True       | True       |             | 45555 |
            | True       | True       |             | fake  |
            | True       | True       | fiware:apps | 45555 |
            | True       | True       | fiware:apps | fake  |


    Scenario Outline: 03: Sync a public image with correct metadata value but only some metadata_set properties (only one)
     Given a new image created in the Glance of master node with name "qatesting01" and this properties
            | param_name      | param_value         |
            | is_public       | True                |
            | sdc_aware       | NULL                |
            | type            | fiware:apps         |
            | nid             | 453                 |
     And   GlanceSync configured to sync images using this configuration parameters:
            | config_section  | config_key          | config_value     |
            | DEFAULT         | metadata_condition  | image.is_public  |
            | DEFAULT         | metadata_set        | <metadata_set>   |
     When  I sync the image
     Then  all images are synchronized
     And   the image "qatesting01" is present in all nodes with the expected data
     And   the properties values of the image "qatesting01" are only the following
            | param_name      | param_value         |
            | <param_name>    | <param_value>       |

            Examples:
            | metadata_set    | param_name | param_value |
            | 'nid'           | nid        | 453         |
            | 'sdc_aware'     | sdc_aware  | NULL        |
            | 'type'          | type       | fiware:apps |
            | 'fake'          |            |             |


    Scenario Outline: 04: Sync a public image with correct metadata value but only some metadata_set properties (2 of them)
     Given a new image created in the Glance of master node with name "qatesting01" and this properties
            | param_name      | param_value         |
            | is_public       | True                |
            | sdc_aware       | NULL                |
            | type            | fiware:apps         |
            | nid             | 453                 |
     And   GlanceSync configured to sync images using this configuration parameters:
            | config_section  | config_key          | config_value     |
            | DEFAULT         | metadata_condition  | image.is_public  |
            | DEFAULT         | metadata_set        | <metadata_set>   |
     When  I sync the image
     Then  all images are synchronized
     And   the image "qatesting01" is present in all nodes with the expected data
     And   the properties values of the image "qatesting01" are only the following
            | param_name      | param_value       |
            | <param_name_1>  | <param_value_1>   |
            | <param_name_2>  | <param_value_2>   |

            Examples:
            | metadata_set           | param_name_1 | param_value_1 | param_name_2 | param_value_2 |
            | 'nid, sdc_aware'       | nid          | 453           | sdc_aware    | NULL          |
            | 'nid, type'            | nid          | 453           | type         | fiware:apps   |
            | 'sdc_aware, type'      | sdc_aware    | NULL          | type         | fiware:apps   |
            | 'sdc_aware, nid'       | sdc_aware    | NULL          | nid          | 453           |
            | 'type, nid'            | type         | fiware:apps   | nid          | 453           |
            | 'type, sdc_aware'      | type         | fiware:apps   | sdc_aware    | NULL          |
            | 'type, fake'           | type         | fiware:apps   |              |               |
            | 'fake, nid'            |              |               | nid          | 453           |
            | 'fake, fake'           |              |               |              |               |