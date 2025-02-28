USE [Test0]
GO
/****** Object:  StoredProcedure [dbo].[usp_CreateOrTruncate_ProcessLogTable]    Script Date: 7/20/2024 2:40:07 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[usp_CreateOrTruncate_ProcessLogTable] (
	-- Add the parameters for the stored procedure here
	 @reset bit
)
AS
BEGIN
	IF OBJECT_ID(N'[dbo].[ProcessLog]', 'U') IS NULL
	BEGIN
	CREATE TABLE [dbo].[ProcessLog] (
		CreateTime datetime2,
		PID int,
		PPID int,
		Name varchar(50),
		[User] varchar(50),
		Status varchar(20),
		InsertTime datetime2
	)
	END
	ELSE
	BEGIN
		IF @reset = 1
		BEGIN
			TRUNCATE TABLE [dbo].[ProcessLog]
		END
	END
END
GO
