USE [Bursatil]
GO

/****** Object:  Table [dbo].[cotizaciones]    Script Date: 16/11/2023 23:11:40 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[cotizaciones](
	[ticker] [char](5) NOT NULL,
	[fecha] [date] NOT NULL,
	[_open] [decimal](10, 4) NULL,
	[_high] [decimal](10, 4) NULL,
	[_low] [decimal](10, 4) NULL,
	[_close] [decimal](10, 4) NULL,
	[volume] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ticker] ASC,
	[fecha] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


